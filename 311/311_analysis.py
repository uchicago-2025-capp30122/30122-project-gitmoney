import pandas as pd

def analyze_311():
    data = pd.read_csv("clean_csv_311_all_cols")
    group_data = data.groupby(['YEAR','CAT','WARD']).size()
    group_data.to_csv("grouped_311",index=False)