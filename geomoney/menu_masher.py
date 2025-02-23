from pathlib import Path
import os
import csv
import json

from .street_search import load_csv


def extract_xsection(location_string:str, all_streets:list):
    """
    This extracts intersections
    """
    match_list = []
    
    ls_list = location_string.split()
    for string in ls_list:
        if string in all_streets:
            match_list.append(string)
        
    return match_list

    


if __name__ == "__main__":

    cwd = Path(os.getcwd())
    menu_money_fp = cwd / "data/menu_money.csv"
    json_fp = cwd / "data/streets.json"

    new_money_menu_fp = cwd / "data/new_menu_money.csv"

    with open(json_fp, 'r', encoding = "utf-8") as jsonfile:
        streets = json.load(jsonfile)

    
    menu_money = load_csv(menu_money_fp)
    allstreets = list(set(streets.keys()))

    new_money_menu = []
    for row in menu_money:
        loc_string = row['description']
        row['xsection'] = extract_xsection(loc_string, allstreets)
        new_money_menu.append(row)
        
    fieldname = new_money_menu[0].keys()
    with open(new_money_menu_fp, 'w', encoding='utf-8') as newfile:
        csvwriter = csv.DictWriter(newfile, fieldnames=fieldname)
        csvwriter.writeheader()
        for row in new_money_menu:
            csvwriter.writerow(row)
