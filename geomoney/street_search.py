
from pathlib import Path
import os
import csv
import json
import re
import ast

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
        # counter = 0
        for row in csvreader:
            # counter += 1
            # if counter >= 100:
            # break
            data.append(row)
        return data


def generate_cross_streets(streets_data, basic = False):
    """ 
    This function generates a dictionary in which the street name indexes a
    list of all cross street names. 
    """
    
    # For each row, make a list containing all segments with same street name
    if basic:
        outpath = Path(os.getcwd()) / "data/streets_basics.json"
        street_dict = dict()

        for row in streets_data:
            street_name = row['STREET_NAM']
            row_necessities = {'FNODE_ID': row['FNODE_ID'],
                            'TNODE_ID': row['TNODE_ID'],
                            'OBJECTID': row['OBJECTID'],
                            'TRANS_ID': row['TRANS_ID'],
                            'PRE_DIR': row['PRE_DIR'],
                            'STREET_NAM': row['STREET_NAM'],
                            'STREET_TYP': row['STREET_TYP'],
                            'F_CROSS': row['F_CROSS'].replace('|', ' '),
                            'T_CROSS': row['T_CROSS'].replace('|', ' '),
                            'MIN_ADDR': min(row['L_F_ADD'],row['R_F_ADD'],row['L_T_ADD'],row['R_T_ADD']),
                            'MAX_ADDR': max(row['L_F_ADD'],row['R_F_ADD'],row['L_T_ADD'],row['R_T_ADD'])}
            if street_name in street_dict:
                street_dict[street_name].append(row_necessities)
            else:
                street_dict[street_name] = [row_necessities]
                
        # Write everything to a jsonfile
        with open(outpath, 'w', encoding='utf-8') as jsonfile:
            json.dump(street_dict, jsonfile, indent=True)
    else:
        outpath = Path(os.getcwd()) / "data/streets.json"
        street_dict = dict()

        for row in streets_data:
            street_name = " ".join([row['PRE_DIR'], row['STREET_NAM'], row['STREET_TYP']])
            row_necessities = {'FNODE_ID': row['FNODE_ID'],
                            'TNODE_ID': row['TNODE_ID'],
                            'OBJECTID': row['OBJECTID'],
                            'TRANS_ID': row['TRANS_ID'],
                            'PRE_DIR': row['PRE_DIR'],
                            'STREET_NAM': row['STREET_NAM'],
                            'STREET_TYP': row['STREET_TYP'],
                            'F_CROSS': row['F_CROSS'].replace('|', ' '),
                            'T_CROSS': row['T_CROSS'].replace('|', ' '),
                            'MIN_ADDR': min(row['L_F_ADD'],row['R_F_ADD'],row['L_T_ADD'],row['R_T_ADD']),
                            'MAX_ADDR': max(row['L_F_ADD'],row['R_F_ADD'],row['L_T_ADD'],row['R_T_ADD'])}
            if street_name in street_dict:
                street_dict[street_name].append(row_necessities)
            else:
                street_dict[street_name] = [row_necessities]
                
        # Write everything to a jsonfile
        with open(outpath, 'w', encoding='utf-8') as jsonfile:
            json.dump(street_dict, jsonfile, indent=True)

def starts_with_directional_prefix(text):
    """
    Check if the given text starts with an optional directional prefix [NSEW]?
    """
    # Define the regex pattern to match the optional directional prefix at the start of the string
    pattern = r'^[NSEW]?\s'
    
    # Use re.match to check if the text starts with the pattern
    if re.match(pattern, text):
        return True
    return False

def street_searcher(main_street, possible_cross = None):
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
    with open(json_fp, 'r', encoding="utf-8") as jsonfile:
        streets = json.load(jsonfile)

    json_fp_basic = Path(os.getcwd()) / "data/streets_basics.json"

    # Opens streets.json and reads the json
    with open(json_fp_basic, 'r', encoding="utf-8") as jsonfile:
        streets_basic = json.load(jsonfile)


    # Searches each street in the list of cross streets -- both to and from --
    # for matches, which are appended to the return list

    if not possible_cross:
        try:
            cross_list = streets[main_street]
            for street in cross_list:
                addr_num = extract_house_number(main_street)
                cross_list = streets[main_street.replace(addr_num, '').strip()]
                if street['MIN_ADDR'] <= addr_num <= street['MAX_ADDR']:
                    rlist.append(street)
        except KeyError:
            rlist.append([])
        
    # Use the main street name to retrieve the list of cross streets
    
    elif isinstance(possible_cross, str):
        try:
            if not starts_with_directional_prefix(main_street):
                cross_list = streets_basic[main_street]
            else:
                cross_list = streets[main_street]
            for street in cross_list:
                tcross = street['T_CROSS'].find(possible_cross)
                fcross = street['F_CROSS'].find(possible_cross)
                if tcross not in [-1, 0] or fcross not in [-1, 0]:
                    rlist.append(street)
        except KeyError:
            rlist.append([])        

    elif isinstance(possible_cross, list):
        if isinstance(main_street, str):
            try:
                if not starts_with_directional_prefix(main_street):
                    cross_list = streets_basic[main_street]
                else:
                    cross_list = streets[main_street]
                for street in cross_list:
                    tcross = street['T_CROSS'].find(possible_cross[0])
                    fcross = street['F_CROSS'].find(possible_cross[1])
                    if tcross not in [-1, 0] and fcross not in [-1, 0]:
                        rlist.append(street)
                    fcross = street['T_CROSS'].find(possible_cross[1])
                    tcross = street['F_CROSS'].find(possible_cross[0])
                    if tcross not in [-1, 0] and fcross not in [-1, 0]:
                        rlist.append(street)
            except KeyError:
                rlist.append([])
        else:
            for main_st in main_street:


                try:
                    if not starts_with_directional_prefix(main_st):
                        cross_list = streets_basic[main_st]
                    else:
                        cross_list = streets[main_st]  
                    for street in cross_list:

                        tcross = street['T_CROSS'].find(possible_cross[0])
                        fcross = street['F_CROSS'].find(possible_cross[1])
                        if tcross not in [-1, 0] and fcross not in [-1, 0]:
                            rlist.append(street)
                        else:
                            fcross = street['T_CROSS'].find(possible_cross[0])
                            tcross = street['F_CROSS'].find(possible_cross[1])
                            if tcross not in [-1, 0] and fcross not in [-1, 0]:
                                rlist.append(street)
                except KeyError:
                    rlist.append([])
    return rlist

def extract_house_number(text):
    """
    Extract the house number from the given address text.
    """
    # Define a pattern to match the house number at the beginning of the string
    pattern = r'^\d+'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    # If a match is found, return the matched number
    if match:
        return match.group()
    
    # If no match is found, return an empty string
    return ''


if __name__ == "__main__":

    cwd = os.getcwd()
    streets_fp = Path(cwd) / 'data/streets.csv'
    menu_money = Path(cwd) / 'data/menu_money.csv'
    new_menu_money = Path(cwd) / 'data/new_menu_money.csv'
    final_menu_money_fp = Path(cwd) / 'data/final_menu_money.csv'
    street_data = load_csv(streets_fp)
    menu_money_data = load_csv(menu_money)
    cross_dict = generate_cross_streets(street_data)
    cross_dict_basic = generate_cross_streets(street_data, True)
    new_menu_money_data = load_csv(new_menu_money)
    final_menu_money = []

    for i, row in enumerate(new_menu_money_data):
        print(f"Processing row {i}")
        menu_addrs = ast.literal_eval(row['addresses'])
        if len(menu_addrs) == 0:
            continue
        elif len(menu_addrs) == 1:
            main_street = menu_addrs[0]
            cross_streets = street_searcher(main_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []
        elif len(menu_addrs) == 2:
            main_street = menu_addrs[0]
            cross_street = menu_addrs[1]
            cross_streets = street_searcher(main_street, cross_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []
        elif len(menu_addrs) == 3:
            main_street = menu_addrs[0]
            cross_street = menu_addrs[1:]
            cross_streets = street_searcher(main_street, cross_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []
        elif len(menu_addrs) == 4:
            main_street = [menu_addrs[0], menu_addrs[2]]
            cross_street = [menu_addrs[1], menu_addrs[3]]
            cross_streets = street_searcher(main_street, cross_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []
        final_menu_money.append(row)
    
    # Unpack values from the 'cross_streets' column and add those columns to the end of each row
    unpacked_final_menu_money = []
    for row in final_menu_money:
        cross_streets = row.get('cross_streets', [])
        if cross_streets:
            for cross_street in cross_streets:
                if isinstance(cross_street, list):
                    new_row = {
                        'year': row['year'],
                        'ward': row['ward'],
                        'cost': row['cost'],
                        'category': row['category'],
                        'program': row['program'],
                        'description': row['description'],
                        'FNODE_ID': '',
                        'TNODE_ID': '',
                        'OBJECTID': '',
                        'TRANS_ID': '',
                        'PRE_DIR': '',
                        'STREET_NAM': '',
                        'STREET_TYP': '',
                        'F_CROSS': '',
                        'T_CROSS': '',
                        'MIN_ADDR': '',
                        'MAX_ADDR': ''
                        }
                else:
                    new_row = {
                        'year': row['year'],
                        'ward': row['ward'],
                        'cost': row['cost'],
                        'category': row['category'],
                        'program': row['program'],
                        'description': row['description'],
                        'FNODE_ID': cross_street.get('FNODE_ID', ''),
                        'TNODE_ID': cross_street.get('TNODE_ID', ''),
                        'OBJECTID': cross_street.get('OBJECTID', ''),
                        'TRANS_ID': cross_street.get('TRANS_ID', ''),
                        'PRE_DIR': cross_street.get('PRE_DIR', ''),
                        'STREET_NAM': cross_street.get('STREET_NAM', ''),
                        'STREET_TYP': cross_street.get('STREET_TYP', ''),
                        'F_CROSS': cross_street.get('F_CROSS', ''),
                        'T_CROSS': cross_street.get('T_CROSS', ''),
                        'MIN_ADDR': cross_street.get('MIN_ADDR', ''),
                        'MAX_ADDR': cross_street.get('MAX_ADDR', '')
                        }
                unpacked_final_menu_money.append(new_row)
    
    # Determine the fieldnames for the CSV file
    fieldnames = ['year', 'ward', 'cost', 'category', 'program', 'description', 'FNODE_ID', 'TNODE_ID', 'OBJECTID', 'TRANS_ID', 'PRE_DIR', 'STREET_NAM', 'STREET_TYP', 'F_CROSS', 'T_CROSS', 'MIN_ADDR', 'MAX_ADDR']
    
    with open(final_menu_money_fp, 'w', encoding='utf-8') as newfile:
        csvwriter = csv.DictWriter(newfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for row in unpacked_final_menu_money:
            csvwriter.writerow(row)