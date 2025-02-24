import json
import polars as pl

def count_wards_years():
    with open("311_clean.json",'r') as file:
        reader = json.load(file)

    df = pl.DataFrame(reader).with_row_index("index")
    print(df)
