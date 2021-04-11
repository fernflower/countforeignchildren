import csv
import sys

import pandas as pd


COLUMN = 'Počet cizinců se zaevidovaným povoleným pobytem  na území ČR (orientační statistické údaje)'
EU_COUNTRIES = [
        "Belgie", "Bulharsko", "Dánsko", "Estonsko", "Finsko", "Chorvatsko", "Irsko", "Itálie", "Kypr",
        "Litva", "Španělsko", "Švédsko", "Maďarsko", "Malta", "	Německo", "Nizozemsko", "Polsko", "Portugalsko",
        "Rakousko", "Rumunsko", "Řecko", "Slovensko", "Slovinsko", "Lotyšsko", "Lucembursko"
]
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


# Magic number explanation: Line 547 is the line with years mapping information, 100 is the column for 2002
def _get_years(df, years_row=547, first_col=3, last_col=-1):
    years = df.iloc[years_row:years_row+1, first_col:last_col].to_dict()
    res = {}
    for col_name, value_dict in years.items():
        res[int(value_dict[years_row])] = col_name
    return res


def do_count(df, first_row, last_row, year, max_age=ADULT_AGE, min_age=0):
    countries = [c for c in df[COLUMN][first_row:last_row].to_list()
                 if isinstance(c, str) and not c.endswith('Celkem')]
    years = _get_years(df)

    r1 = year - max_age + 1
    r2 = year - min_age + 1
    children_columns = [c for y, c in years.items() if y in range(r1, r2)]
    children_long_term_residence = {}
    # XXX FIXME there should be a fancy way to keep country name together with the data
    sums = df.iloc[first_row:last_row,:].loc[df[COLUMN].isin(countries), children_columns].sum(axis=1).to_list()
    for i, country in enumerate(countries):
        children_long_term_residence[country] = int(sums[i])
    # filter out EU countries
    non_eu = [c for c in countries if c not in EU_COUNTRIES]
    sum_non_eu = sum(children_long_term_residence[c] for c in countries if c in non_eu)
    print(f"Foreigners (visa over 90 days and long-term residence) from non-EU countries "
          f"born {r1} - {r2 - 1} by 31/12/{year} - {sum_non_eu}")
    return sum_non_eu


def main(args=sys.argv[1:]):
    if not args:
        raise ProcessError("Please pass an xlsx file as first argument")
    xl_file = pd.read_excel(args[0], sheet_name=None)
    df = xl_file['pobyt_31.12.2019-2020']
    total_expenses = 0
    total_premiums = 0
    year = 2019
    first_row_map = {2019: 5, 2020: 548}
    last_row_map = {2019: 542, 2020: -1}
    age_ranges = [(r, r+5) for r in range(0, 95, 5)] + [(95, None)]
    with open(OUT, 'w', newline='') as csvfile:
        fieldnames = ['Age group', 'Avg cost per person', 'Total foreigners', 'Total expenses (mln czk)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, (r1, r2) in enumerate(age_ranges):
            if r1 == 95:
                group_size = do_count(df, first_row_map[year], last_row_map[year], year, max_age=142, min_age=r1)
                avg_price = EXPENSES_PER_AGE_GROUP[(95, None)]
                age_group = '95+'
            else:
                group_size = do_count(df, first_row_map[year], last_row_map[year], year, max_age=r2, min_age=r1)
                avg_price = EXPENSES_PER_AGE_GROUP[(r1, r2 - 1)]
                age_group = f'{r1}-{r2-1}'
            group_expenses = avg_price * group_size
            writer.writerow({'Age group': age_group,
                             'Total expenses (mln czk)': group_expenses/10**6,
                             'Total foreigners': group_size,
                             'Avg cost per person': avg_price})


if __name__ == '__main__':
    main()
