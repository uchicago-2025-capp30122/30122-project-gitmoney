import httpx
import numpy as np
import pandas as pd
from pathlib import Path
import pathlib
import os
import pandas as pd
import csv
import json




def load_csv(path_to_csv: Path):
    """
    Read a .csv file from a filepath. 

    Args:
    - path_to_csv (Path): a constructed filepath to the .csv
    Returns a List of rows in dict format
    """
    data = []
    with open(path_to_csv, 'r', encoding="utf-8") as filereader:
        csvreader = csv.DictReader(filereader)
        counter = 0
        for row in csvreader:
            counter += 1
            if counter >= 100:
                break
            data.append(row)
        return data

def generate_cross_streets(streets_data):
    """
    This function generates a dictionary in which the key name indexes a
    list of cross street names. 
    """

    outpath = Path(os.getcwd()) / "data/streets.json"



    street_dict = dict()

    for row in streets_data:
        if row['STREET_NAM'] not in street_dict.keys():
            street_dict[row['STREET_NAM']] = [row]
        else:
            street_dict[row['STREET_NAM']].append(row)

    with open(outpath, 'w', encoding = 'utf-8') as jsonfile:
        json.dump(street_dict, jsonfile, indent = True)



def street_searcher(main_street, possible_cross):
    rlist = []
    json_fp = Path(os.getcwd()) / "data/streets.json"

    with open(json_fp, 'r', encoding = "utf-8") as jsonfile:
        streets = json.load(jsonfile)
    cross_list = streets[main_street]
    for street in cross_list:
        tcross = street['T_CROSS'].find(possible_cross)
        fcross = street['F_CROSS'].find(possible_cross)
        print(f"fcross: {fcross}; tcross: {tcross}")
        if tcross or fcross:
            rlist.append(street)
    return rlist



    
        




if __name__ == "__main__":
    cwd = os.getcwd()
    streets_fp = Path(cwd) / 'data/streets.csv'
    menu_money = Path(cwd) / 'data/menu_money.csv'
    csv_rows = load_csv(streets_fp)
    menu_money = load_csv(menu_money)
    generate_cross_streets(csv_rows)
    print(street_searcher("NORTH","MOODY"))
    