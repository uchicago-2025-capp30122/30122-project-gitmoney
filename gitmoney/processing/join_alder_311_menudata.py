import pandas as pd
import re
import json
import os
import pathlib
import csv
import processing.wiki_scraper as wiki

data_file = pathlib.Path(__file__).parent.parent / "data/"

def join_calls_alders():
    """
    Joins data with each alderperson to a database with calls for
    """
    
    # Read in data
    calls_money = pd.read_csv(data_file/"calls_money.csv")
    alders = pd.read_csv(data_file/"all_alderpeople_2018_23.csv")
    
    # Ensure joining columns are of same type
    calls_money['year']=calls_money['year'].astype(int)
    calls_money['ward']=calls_money['ward'].astype(int)
    
    alders['Clean Ward']=alders['Clean Ward'].astype(int)
    alders['filled_year']=alders['filled_year'].astype(int)
    
    # Join Data
    joined = pd.merge(alders, calls_money, \
        left_on=["Clean Ward", "filled_year"], right_on=["ward", "year"])
    joined = joined.loc[(joined['filled_year'] >= 2018)]
    
    # Select only necessary columns
    joined_clean = joined.loc[:, ['Clean Ward', 'Alderperson', 'Start Date', \
        'End Date', 'filled_year', 'year', 'category', 'calls',\
            'num_projects', 'total_cost']]

    joined_clean= joined_clean.sort_values(["Clean Ward", "year",])
    joined_clean = joined_clean.reset_index(drop=True)
    
    joined_clean.to_csv(data_file/"calls_money_pivot_with_alder.csv")
    

