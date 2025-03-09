
from pathlib import Path
import os
import csv
import json
import re
import ast


def convert_cost(cost):
    try:
        # first remove any currency symbols and commas
        cost_str = cost.replace('$', '').replace(',', '')
        cost_float = float(cost_str)

    except (ValueError, TypeError):
        # if conversion fails, set to 0
        cost_float = 0.0

    return cost_float


def load_csv(path_to_csv: Path):
    """
    Read a .csv file from a filepath. This is used to load menu_money and 
    streets data.

    Args:
    - path_to_csv (Path): a constructed filepath to the .csv
        
    Returns: a List of rows in dict format
    """

    # initialize return list, open and read the csv.
    data = []
    with open(path_to_csv, 'r', encoding="utf-8") as filereader:
        csvreader = csv.DictReader(filereader)
        for row in csvreader:
            data.append(row)
        return data


def generate_cross_streets(streets_data, basic = False):
    """ 
    This function generates a dictionary in which the street name indexes a
    list of all cross street names. 

    Args:
    - streets_data (list of dicts): This is the data from the streets.csv file
    - basic (bool): If True, the dictionary will not have street dir or suffix

    Returns:
    - street_dict (dict): This is the dictionary with street names as keys
        and lists of cross streets as values.
    """
    
    # if basic is True, the dictionary will not have street dir or suffix
    if basic:
        outpath = Path(os.getcwd()) / "gitmoney/data/streets_basics.json"
        street_dict = dict()

        # for each row, make a list containing all segments with same street name
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
            
            # append the dict to the return-list
            if street_name in street_dict:
                street_dict[street_name].append(row_necessities)
            else:
                street_dict[street_name] = [row_necessities]
                
        # write everything to a jsonfile
        with open(outpath, 'w', encoding='utf-8') as jsonfile:
            json.dump(street_dict, jsonfile, indent=True)
    else:
        outpath = Path(os.getcwd()) / "gitmoney/data/streets.json"
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

    Args:
    - text (str): The text to check

    Returns:
    - bool: True if the text starts with an optional directional prefix, False otherwise
    """
    # define the regex pattern to match the optional directional prefix
    pattern = r'^[NSEW]?\s'
    
    # use re.match to check if the text starts with the pattern
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

    Returns:
    - rlist (list of dicts): This is a list of dictionaries containing the
        cross streets. If no cross streets are found, the list will be empty.
    """

    # generates the return list and the json filepath for streets.json
    rlist = []
    json_fp = Path(os.getcwd()) / "gitmoney/data/streets.json"

    # opens streets.json and reads the json
    with open(json_fp, 'r', encoding="utf-8") as jsonfile:
        streets = json.load(jsonfile)

    json_fp_basic = Path(os.getcwd()) / "gitmoney/data/streets_basics.json"

    # opens streets.json and reads the json
    with open(json_fp_basic, 'r', encoding="utf-8") as jsonfile:
        streets_basic = json.load(jsonfile)


    # searches each street in the list of cross streets -- both to and from --
    # for matches, which are appended to the return list

    if not possible_cross:
        try:
            # check if the street name starts with a number (single address)
            addr_num = extract_house_number(main_street)

            # remove the address number from the street name
            main_street_truncated = main_street.replace(addr_num, '')

            # use the truncated street name to make basic list of cross streets
            cross_list = streets[main_street_truncated.strip()]

            # check the address number against address numbers for that block
            for street in cross_list:
                min_addr = int(street['MIN_ADDR'])
                if min_addr == 0:
                    continue
                max_addr = int(street['MAX_ADDR'])
                #append the street if the address number is within the range
                if min_addr <= int(addr_num) <= max_addr:
                    rlist.append(street)

        # raise exceptions if the street name is not found in the json
        except (KeyError, ValueError) as e:
            rlist.append([])

    # if one main and one cross street are given
    elif isinstance(possible_cross, str):
        # check if the street name starts with a direction prefix
        try:
            # make the list of cross streets
            if not starts_with_directional_prefix(main_street):
                cross_list = streets_basic[main_street]
            else:
                cross_list = streets[main_street]

            # search the list of cross streets for the cross street
            for street in cross_list:
                tcross = street['T_CROSS'].find(possible_cross)
                fcross = street['F_CROSS'].find(possible_cross)

                # append either side of the intersection
                if tcross not in [-1, 0] or fcross not in [-1, 0]:
                    rlist.append(street)

        # raise exceptions if the street name is not found in the json
        except KeyError:
            rlist.append([])

    # if one main and two cross streets are given
    elif isinstance(possible_cross, list):
        if isinstance(main_street, str):
            # check if the street name starts with a direction prefix
            try:
                # make the list of cross streets
                if not starts_with_directional_prefix(main_street):
                    cross_list = streets_basic[main_street]
                else:
                    cross_list = streets[main_street]

                # search the list of cross streets for the cross street
                for street in cross_list:
                    tcross = street['T_CROSS'].find(possible_cross[0])
                    fcross = street['F_CROSS'].find(possible_cross[1])
                    
                    # check if both cross streets are found
                    if tcross not in [-1, 0] and fcross not in [-1, 0]:
                        rlist.append(street)

                    # check if both cross streets are found in reverse order
                    fcross = street['T_CROSS'].find(possible_cross[1])
                    tcross = street['F_CROSS'].find(possible_cross[0])
                    if tcross not in [-1, 0] and fcross not in [-1, 0]:
                        rlist.append(street)

            # raise exceptions if the street name is not found in the json
            except KeyError:
                rlist.append([])

        # if four streets are given, two main and two cross streets
        else:
            for main_st in main_street:
                try:
                    # make the list of cross streets
                    if not starts_with_directional_prefix(main_st):
                        cross_list = streets_basic[main_st]
                    else:
                        cross_list = streets[main_st]  

                    # search the list of cross streets for the cross street
                    for street in cross_list:
                        tcross = street['T_CROSS'].find(possible_cross[0])
                        fcross = street['F_CROSS'].find(possible_cross[1])

                        # check if both cross streets are found
                        if tcross not in [-1, 0] and fcross not in [-1, 0]:
                            rlist.append(street)
                        # check if both cross streets are found in reverse order
                        else:
                            fcross = street['T_CROSS'].find(possible_cross[0])
                            tcross = street['F_CROSS'].find(possible_cross[1])
                            if tcross not in [-1, 0] and fcross not in [-1, 0]:
                                rlist.append(street)
                
                # raise exceptions if the street name is not found in the json
                except KeyError:
                    rlist.append([])
    
    # all matches are returned
    return rlist


def extract_house_number(text):
    """
    Extract the house number from the given address text.

    Args:
    - text (str): The address text to extract the house number from

    Returns:
    - str: The extracted house number
    """
    # Define a pattern to match the house number at the beginning of the string
    pattern = r'^\d+'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    # If a match is found, return the matched number
    if match:
        return match.group()
    
    # If no match is found, return an empty string
    return '0'


def street_search(new_menu_money_data, streets_fp):
    """
    This function runs the street_searcher function on the new_menu_money_data
    and returns a list of dictionaries with the cross streets appended. It then
    unpacks the cross streets and appends them to the end of each row in the
    new_menu_money_data list (making tidy data). The function also returns the
    fieldnames for the CSV file.

    Args:
    - new_menu_money_data (list of dicts): The data to be processed
    - streets_fp (Path): The filepath to the streets.json file

    Returns:
    - unpacked_final_menu_money (list of dicts): The processed data
    - fieldnames (list): The fieldnames for the CSV file
    """
    # return-list
    final_menu_money = [] 

    # run street_searcher on each row in the new_menu_money_data
    for i, row in enumerate(new_menu_money_data):
        print(f"Processing row {i}")
        menu_addrs = ast.literal_eval(row['addresses'])

        # check the length of the list of addresses, skip if empty
        if len(menu_addrs) == 0:
            continue

        # if one address is given
        elif len(menu_addrs) == 1:
            main_street = menu_addrs[0]
            cross_streets = street_searcher(main_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []

        # if two addresses are given
        elif len(menu_addrs) == 2:
            main_street = menu_addrs[0]
            cross_street = menu_addrs[1]
            cross_streets = street_searcher(main_street, cross_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []

        # if three addresses are given
        elif len(menu_addrs) == 3:
            main_street = menu_addrs[0]
            cross_street = menu_addrs[1:]
            cross_streets = street_searcher(main_street, cross_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []
        
        # if four addresses are given
        elif len(menu_addrs) == 4:
            main_street = [menu_addrs[0], menu_addrs[2]]
            cross_street = [menu_addrs[1], menu_addrs[3]]
            cross_streets = street_searcher(main_street, cross_street)
            if cross_streets:
                row['cross_streets'] = cross_streets
            else:
                row['cross_streets'] = []

        final_menu_money.append(row)
    
    # return-list
    unpacked_final_menu_money = []

    # unpack values from the 'cross_streets' column 
    # and add those columns to the end of each row to make tidy data
    for row in final_menu_money:

        # check if the cross_streets column is empty
        cross_streets = row.get('cross_streets', [])

        # if the cross_streets column is not empty
        if cross_streets:
            # for each cross street, append a new row to the return-list
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
    fieldnames = [
        'year',
        'ward',
        'cost',
        'category',
        'program',
        'description',
        'FNODE_ID',
        'TNODE_ID',
        'OBJECTID',
        'TRANS_ID',
        'PRE_DIR',
        'STREET_NAM',
        'STREET_TYP',
        'F_CROSS',
        'T_CROSS',
        'MIN_ADDR',
        'MAX_ADDR'
        ]
    return unpacked_final_menu_money, fieldnames

def main():

    # define the filepaths
    final_menu_money_fp = Path.cwd() / 'gitmoney/data/final_menu_money.csv'
    streets_fp = Path.cwd() / 'gitmoney/data/streets.csv'
    menu_money = Path.cwd() / 'gitmoney/data/menu_money.csv'
    new_menu_money = Path.cwd()/ 'gitmoney/data/new_menu_money.csv'
    
    # load the data
    street_data = load_csv(streets_fp)
    menu_money_data = load_csv(menu_money)
    cross_dict = generate_cross_streets(street_data)
    cross_dict_basic = generate_cross_streets(street_data, True)
    new_menu_money_data = load_csv(new_menu_money)

    # run the street_search function
    unpacked_final_menu_money, fieldnames = street_search(new_menu_money_data, streets_fp)

    # write the data to a new CSV file
    with open(final_menu_money_fp, 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for row in unpacked_final_menu_money:
            csvwriter.writerow(row)


if __name__ == "__main__":
    main()