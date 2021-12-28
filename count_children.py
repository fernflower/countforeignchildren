import argparse
import csv
import sys

import pandas as pd


COLUMN = 'Počet cizinců se zaevidovaným povoleným pobytem  na území ČR (orientační statistické údaje)'
EU_COUNTRIES = {
        "Belgie", "Bulharsko", "Dánsko", "Estonsko", "Finsko", "Chorvatsko", "Irsko", "Itálie", "Kypr",
        "Litva", "Španělsko", "Švédsko", "Maďarsko", "Malta", "	Německo", "Nizozemsko", "Polsko", "Portugalsko",
        "Rakousko", "Rumunsko", "Řecko", "Slovensko", "Slovinsko", "Lotyšsko", "Lucembursko"
}
ADULT_AGE = 18
# According to Výsledky zdravotnických účtů ČR - 2010–2019
# https://www.czso.cz/csu/czso/vysledky-zdravotnickych-uctu-cr-m6hwrlzbbw ,
# average numbers calculated
EXPENSES_PER_AGE_GROUP = {
        # economically inactive: children
        (0, 4): 21084,
        (5, 9): 11209.5,
        (10, 14): 12322,
        (15, 18): 13647.5,  # approximation, will take same value as (15, 19)
        (15, 19): 13647.5,
        # economically active
        (20, 24): 12600,
        (25, 29): 15192.5,
        (30, 34): 17076,
        (35, 39): 17460,
        (40, 44): 18488.5,
        (45, 49): 21865.5,
        (50, 54): 26685.5,
        (55, 59): 32562,
        (60, 64): 40524.5,
        # economically inactive: retired
        (65, 69): 50573.5,
        (70, 74): 61911.5,
        (75, 79): 72105,
        (80, 84): 76047,
        (85, 89): 82282.5,
        (90, 94): 85478,
        (95, None): 90975  # all people over 95+ fall under this category
}
PREMIUM_OBZP_2019 = 1803 * 12
OUT = 'out.csv'


class ProcessError(Exception):
    pass


# Magic number explanation: Line 547 is the line with years mapping information, 3 is first column with data
def _get_years(df, years_row=547, first_col=3, last_col=-1):
    years = df.iloc[years_row:years_row+1, first_col:last_col].to_dict()
    res = {}
    for col_name, value_dict in years.items():
        res[int(value_dict[years_row])] = col_name
    return res


def do_count(df, first_row, last_row, year, max_age=ADULT_AGE, min_age=0, non_eu_only=True):
    """
    Count foreigners in [min_age, max_age) interval.
    Make sure you increment expected max_age by 1 to get [min_age, max_age] range.
    """
    countries = [c for c in df[COLUMN][first_row:last_row].to_list()
                 if isinstance(c, str) and not c.endswith('Celkem')]
    years = _get_years(df)

    r1 = year - max_age + 1
    r2 = year - min_age + 1
    children_columns = [c for y, c in years.items() if y in range(r1, r2)]
    # result will be kept here
    children_long_term_residence = {}
    children_total = 0
    # XXX FIXME there should be a fancy way to keep country name together with the data
    sums = df.iloc[first_row:last_row,:].loc[df[COLUMN].isin(countries), children_columns].sum(axis=1).to_list()
    for i, country in enumerate(countries):
        children_long_term_residence[country] = int(sums[i])
    if non_eu_only:
        # filter out EU countries
        non_eu = [c for c in countries if c not in EU_COUNTRIES]
        sum_non_eu = sum(children_long_term_residence[c] for c in countries if c in non_eu)
        children_long_term_residence = {c: v for c, v in children_long_term_residence.items() if c in non_eu}
    selection = 'non EU' if non_eu_only else 'all'
    children_total = sum(v for c, v in children_long_term_residence.items())
    print(f"Foreigners (visa over 90 days and long-term residence) from {selection} countries "
          f"born {r1} - {r2 - 1} by 31/12/{year} - {children_total}")
    return children_total, children_long_term_residence


def get_mapping(filename, max_age, min_age, non_eu_only, year, first_row, last_row):
    xl_file = pd.read_excel(filename, sheet_name=None)
    df = xl_file['pobyt_31.12.2019-2020']
    group_size, full_mapping = do_count(df, first_row, last_row, year,
                                        max_age=max_age, min_age=min_age, non_eu_only=non_eu_only)
    return full_mapping


def parse_args(args):
    parser = argparse.ArgumentParser(description='Parse foreigners/age/country information')
    parser.add_argument('--file', help='Path to an excel file with data',
                        default='priloha_882435642_1_TDU_věk_2019-2020.xlsx')
    parser.add_argument('--min-age', help='Minimal age of foreigners to consider', default=0, type=int)
    parser.add_argument('--max-age', help='Maximum age of foreigners to consider', default=18, type=int)
    parser.add_argument('--non-eu', help='Filter out EU citizens', action='store_true')
    parser.add_argument('--year', help='Year to get data for', default=2019, choices=[2019, 2020], type=int)
    parser.add_argument('--output', help='Filename for resulting csv with expenses per age group', default=OUT)
    parser.add_argument('--csv', help='Run in generate expenses output mode', action='store_true')
    return parser.parse_args(args)


def process_interval(parsed_args, first_row_map, last_row_map):
    return get_mapping(filename=parsed_args.file, max_age=parsed_args.max_age + 1, min_age=parsed_args.min_age,
                       non_eu_only=parsed_args.non_eu, year=parsed_args.year,
                       first_row=first_row_map[parsed_args.year], last_row=last_row_map[parsed_args.year])


def generate_expenses_csv(parsed_args, first_row_map, last_row_map):
    # XXX FIXME Doesn't really support --max-age\--min-age yet, max_age and min_age must be aligned with
    # EXPENSES_PER_AGE_GROUP intervals
    age_ranges = [(r, r+5) for r in range(0, parsed_args.max_age + 1, 5)]
    if parsed_args.max_age > 95:
        age_ranges.append((95, None))
    with open(parsed_args.output, 'w', newline='') as csvfile:
        fieldnames = ['Age group', 'Avg cost per person', 'Total foreigners', 'Total expenses (mln czk)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for (r1, r2) in age_ranges:
            if r1 == 95:
                group_mapping = get_mapping(filename=parsed_args.file,
                                            max_age=142,
                                            min_age=r1,
                                            non_eu_only=parsed_args.non_eu, year=parsed_args.year,
                                            first_row=first_row_map[parsed_args.year],
                                            last_row=last_row_map[parsed_args.year])
                group_size = sum(v for k, v in group_mapping.items())
                avg_price = EXPENSES_PER_AGE_GROUP[(95, None)]
                age_group = '95+'
            else:
                group_mapping = get_mapping(filename=parsed_args.file,
                                            max_age=r2,
                                            min_age=r1,
                                            non_eu_only=parsed_args.non_eu, year=parsed_args.year,
                                            first_row=first_row_map[parsed_args.year],
                                            last_row=last_row_map[parsed_args.year])
                group_size = sum(v for k, v in group_mapping.items())
                avg_price = EXPENSES_PER_AGE_GROUP[(r1, r2 - 1)]
                age_group = f'{r1}-{r2-1}'
            group_expenses = avg_price * group_size
            writer.writerow({'Age group': age_group,
                             'Total expenses (mln czk)': group_expenses/10**6,
                             'Total foreigners': group_size,
                             'Avg cost per person': avg_price})


def run(args=sys.argv[1:]):
    first_row_map = {2019: 5, 2020: 548}
    last_row_map = {2019: 542, 2020: -1}
    parsed_args = parse_args(args)
    if parsed_args.csv:
        generate_expenses_csv(parsed_args, first_row_map, last_row_map)
    else:
        process_interval(parsed_args, first_row_map, last_row_map)


if __name__ == '__main__':
    run()
