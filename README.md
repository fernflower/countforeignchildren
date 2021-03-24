## About
A script to comfortably query [xlsx file with the latest foreigners statistics](priloha_882435642_1_TDU_věk_2019-2020.xlsx) requested from Ředitelství služby cizinecké policie (thank you, plk. Ing. Milena Křivánková Beranová and pplk. Mgr. Zdeněk Soudek!).


## How to run it

In a python 3.6+ virtualenv:
1. Install requirements with `pip install -r requirements.txt`
2. Run the script with `python count_children.py priloha_882435642_1_TDU_věk_2019-2020.xlsx`

The output format might change slightly, but should be similar to:
```
Stats for age group 0 - 18:
Children (visa over 90 days and long-term residence) from non-EU countries born 2002 - 2019 by 31/12/2019 - 11581
Children (visa over 90 days and long-term residence) from non-EU countries born 2003 - 2020 by 31/12/2020 - 14066
Stats for age group 0 - 15:
Children (visa over 90 days and long-term residence) from non-EU countries born 2005 - 2019 by 31/12/2019 - 9466
Children (visa over 90 days and long-term residence) from non-EU countries born 2006 - 2020 by 31/12/2020 - 11330
```
