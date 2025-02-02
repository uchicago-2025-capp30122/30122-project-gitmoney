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
    Read a .csv file from a filepath. This is used to load menu_money and 
    streets data.

    Args:
    - path_to_csv (Path): a constructed filepath to the .csv
    Returns a List of rows in dict format
    """

    # Initialize return list, open and read the csv.
    data = []
    with open(path_to_csv, 'r', encoding="utf-8") as filereader:
        csvreader = csv.DictReader(filereader)
        #counter = 0
        for row in csvreader:
            #counter += 1
            #if counter >= 100:
                #break
            data.append(row)
        return data

def generate_cross_streets(streets_data):
    """
    This function generates a dictionary in which the street name indexes a
    list of all cross street names. 
    """

    outpath = Path(os.getcwd()) / "data/streets.json"
    street_dict = dict()

    # For each row, make a list containing all segments with same street name
    for row in streets_data:
        row_necessities = {'FNODE_ID': row['FNODE_ID'],
            'TNODE_ID': row['TNODE_ID'],
            'OBJECTID': row['OBJECTID'],
            'TRANS_ID': row['TRANS_ID'],
            'STREET_NAM': row['STREET_NAM'],
            'F_CROSS': row['F_CROSS'],
            'T_CROSS': row['T_CROSS']}
        if row['STREET_NAM'] in street_dict.keys():
            street_dict[row['STREET_NAM']].append(row_necessities)
        else:
            street_dict[row['STREET_NAM']] = [row_necessities]
            
    # Write everything to a jsonfile
    with open(outpath, 'w', encoding = 'utf-8') as jsonfile:
        json.dump(street_dict, jsonfile, indent = True)



def street_searcher(main_street, possible_cross):
    """
    This function will access the streets.json file created by 
    generate_cross_streets. 

    Args:
    - main_street (str uppercase): This is the main street name. Used as key
        in streets.json to access a list of cross streets 
    - possible_cross (str uppercase): This is the name of the cross street 
        being searched.
    """

    # Generates the return list and the json filepath for streets.json
    rlist = []
    json_fp = Path(os.getcwd()) / "data/streets.json"

    # Opens streets.json and reads the json
    with open(json_fp, 'r', encoding = "utf-8") as jsonfile:
        streets = json.load(jsonfile)

    # Use the main street name to retrieve the list of cross streets
    cross_list = streets[main_street]

    # Searches each street in the list of cross streets -- both to and from --
    # for matches, which are appended to the return list
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