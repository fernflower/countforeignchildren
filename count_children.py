import sys

import pandas as pd


COLUMN = 'Počet cizinců se zaevidovaným povoleným pobytem  na území ČR (orientační statistické údaje)'
EU_COUNTRIES = [
        "Belgie", "Bulharsko", "Dánsko", "Estonsko", "Finsko", "Chorvatsko", "Irsko", "Itálie", "Kypr",
        "Litva", "Španělsko", "Švédsko", "Maďarsko", "Malta", "	Německo", "Nizozemsko", "Polsko", "Portugalsko",
        "Rakousko", "Rumunsko", "Řecko", "Slovensko", "Slovinsko", "Lotyšsko", "Lucembursko"
]


class ProcessError(Exception):
    pass


# Magic number explanation: Line 547 is the line with years mapping information, 100 is the column for 2002
def _get_years(df, years_row=547, first_col=100, last_col=-1):
    years = df.iloc[years_row:years_row+1, first_col:last_col].to_dict()
    res = {}
    for col_name, value_dict in years.items():
        res[int(value_dict[years_row])] = col_name
    return res


def do_count(df, first_row, last_row, year, max_age=18):
    countries = [c for c in df[COLUMN][first_row:last_row].to_list()
                 if isinstance(c, str) and not c.endswith('Celkem')]
    years = _get_years(df)

    children_columns = [c for y, c in years.items() if y in range(year-max_age+1,year+1)]
    children_long_term_residence = {}
    # XXX FIXME there should be a fancy way to keep country name together with the data
    sums = df.iloc[first_row:last_row,:].loc[df[COLUMN].isin(countries), children_columns].sum(axis=1).to_list()
    for i, country in enumerate(countries):
        children_long_term_residence[country] = int(sums[i])
    # filter out EU countries
    non_eu = [c for c in countries if c not in EU_COUNTRIES]
    sum_non_eu = sum(children_long_term_residence[c] for c in countries if c in non_eu)
    print(f"Children (visa over 90 days and long-term residence) from non-EU countries "
          f"born {year - max_age + 1} - {year} by 31/12/{year} - {sum_non_eu}")


def main(args=sys.argv[1:]):
    if not args:
        raise ProcessError("Please pass an xlsx file as first argument")
    xl_file = pd.read_excel(args[0], sheet_name=None)
    df = xl_file['pobyt_31.12.2019-2020']
    print("Stats for age group 0 - 18:")
    do_count(df, 5, 542, 2019)
    do_count(df, 548, -1, 2020)
    print("Stats for age group 0 - 15:")
    do_count(df, 5, 542, 2019, 15)
    do_count(df, 548, -1, 2020, 15)

if __name__ == '__main__':
    main()
