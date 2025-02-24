import json
import polars as pl
import pandas as pd


def count_wards_years():
    with open("311_clean.json",'r') as file:
        reader = json.load(file)

    df = pl.DataFrame(reader).with_row_index("index")
    print(df.group_by(['cat','ward','year']).count())

    print(df.select(pl.col("year").unique()))

    print(df.shape)

def check_og_data():
    with open("311_data.json",'r') as file:
        reader = json.load(file)
    my_list = []
    count = 0
    for call in reader:
        my_list.append(call)
        count += 1
        if count == 20000:
            break

    return pd.DataFrame(my_list)
    
