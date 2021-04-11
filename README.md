## About
A script to comfortably query [xlsx file with the latest foreigners statistics](priloha_882435642_1_TDU_věk_2019-2020.xlsx) requested from Ředitelství služby cizinecké policie (thank you, plk. Ing. Milena Křivánková Beranová and pplk. Mgr. Zdeněk Soudek!).


## How to run it

In a python 3.6+ virtualenv:
1. Install requirements with `pip install -r requirements.txt`
2. Run the script with `python count_children.py priloha_882435642_1_TDU_věk_2019-2020.xlsx`

The script will produce an out.csv with the following information: foreigners (visa over 90 days and long-term residence)
numbers for different age groups and VZP expenses for those groups in year 2019.

## Additional information

Futher calculations, better representation and diagrams can be found at 
[The 2019 foreigners VZP contributions&expenses analysis](https://docs.google.com/spreadsheets/d/1k0ynJQ6F30v-cjznDTgPboe1Ug31DsXN6PRjgQXilw8).

Comments and reviews are welcome!

```
Age group,Avg cost per person,Total foreigners,Total expenses (mln czk)
0-4,21084,3571,75.290964
5-9,11209.5,3369,37.7648055
10-14,12322,2526,31.125372
15-19,13647.5,7573,103.3525175
20-24,12600,22780,287.028
25-29,15192.5,28269,429.4767825
30-34,17076,25265,431.42514
35-39,17460,20690,361.2474
40-44,18488.5,16502,305.097227
45-49,21865.5,13168,287.924904
50-54,26685.5,9599,256.1541145
55-59,32562,6823,222.170526
60-64,40524.5,3468,140.538966
65-69,50573.5,2004,101.349294
70-74,61911.5,1343,83.1471445
75-79,72105,879,63.380295
80-84,76047,419,31.863693
85-89,82282.5,177,14.5640025
90-94,85478,76,6.496328
95+,90975,29,2.638275
```
