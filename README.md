## About
A script to comfortably query [xlsx file with the latest foreigners statistics](priloha_882435642_1_TDU_věk_2019-2020.xlsx) requested from Ředitelství služby cizinecké policie (thank you, plk. Ing. Milena Křivánková Beranová and pplk. Mgr. Zdeněk Soudek!).


## How to run it

In a python 3.6+ virtualenv:
1. Install requirements with `pip install -r requirements.txt`
2. Run the script. Currently two modes are supported controlled by --csv flag: to process data from the select age
interval and generate csv with expenses per specific age groups.

```
python count_children.py --file priloha_882435642_1_TDU_věk_2019-2020.xlsx  --non-eu --year 2020 --max-age=17 --min-age=0`

Foreigners (visa over 90 days and long-term residence) from non EU countries born 2003 - 2020 by 31/12/2020 - 13339
```

```
python count_children.py  --file priloha_882435642_1_TDU_věk_2019-2020.xlsx  --year 2020 --max-age=95 --min-age=0 --csv --non-eu
```

The script will produce an out.csv with the following information: foreigners (visa over 90 days and long-term residence)
numbers for different age groups and VZP expenses for those groups in year 2019.

## Additional information

Futher calculations, better representation and diagrams can be found at 
[The 2019 foreigners VZP contributions&expenses analysis](https://docs.google.com/spreadsheets/d/1k0ynJQ6F30v-cjznDTgPboe1Ug31DsXN6PRjgQXilw8).

Comments and reviews are welcome!


### Data for year 2019

```
Age group,Avg cost per person,Total foreigners,Total expenses (mln czk)
0-4,21084,3440,72.52896
5-9,11209.5,3176,35.601372
10-14,12322,2312,28.488464
15-19,13647.5,7334,100.090765
20-24,12600,22473,283.1598
25-29,15192.5,27267,414.2538975
30-34,17076,23221,396.521796
35-39,17460,17908,312.67368
40-44,18488.5,13960,258.09946
45-49,21865.5,10999,240.4986345
50-54,26685.5,7299,194.7774645
55-59,32562,4706,153.236772
60-64,40524.5,2002,81.130049
65-69,50573.5,833,42.1277255
70-74,61911.5,512,31.698688
75-79,72105,295,21.270975
80-84,76047,162,12.319614
85-89,82282.5,74,6.088905
90-94,85478,27,2.307906
95+,90975,7,0.636825
```

### Data for year 2020 (expenses rate taken from year 2019 as no new data yet)

```
Age group,Avg cost per person,Total foreigners,Total expenses (mln czk)
0-4,21084,3845,81.06798
5-9,11209.5,3995,44.7819525
10-14,12322,2914,35.906308
15-19,13647.5,10052,137.18467
20-24,12600,24775,312.165
25-29,15192.5,32094,487.588095
30-34,17076,27653,472.202628
35-39,17460,21634,377.72964
40-44,18488.5,16832,311.198432
45-49,21865.5,13187,288.3403485
50-54,26685.5,8794,234.672287
55-59,32562,5457,177.690834
60-64,40524.5,2306,93.449497
65-69,50573.5,936,47.336796
70-74,61911.5,553,34.2370595
75-79,72105,303,21.847815
80-84,76047,172,13.080084
85-89,82282.5,87,7.1585775
90-94,85478,39,3.333642
95+,90975,11,1.000725
```
