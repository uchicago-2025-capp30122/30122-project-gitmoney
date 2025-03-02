from pathlib import Path
import os
import pandas as pd

cwd = Path(os.getcwd()).parent
file_fp = cwd/'data/calls_money.csv'

data = pd.read_csv(file_fp)
data = data[(data['year'] > 2017) & (data['year'] < 2024)]

ward_year = data.groupby(["year",'ward','category']).agg({
    'calls':"sum",
    'total_cost':"sum"}).reset_index()
ward_year["calls_pct"] = ward_year["calls"] / ward_year.groupby(["year","ward"])["calls"].transform("sum") * 100
ward_year["cost_pct"] = ward_year["total_cost"] / ward_year.groupby(["year","ward"])["total_cost"].transform("sum") * 100

print(ward_year)