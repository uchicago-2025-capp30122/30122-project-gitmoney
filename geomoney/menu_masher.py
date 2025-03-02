from street_search import load_csv
from pathlib import Path
import os
import csv
import json
import re
import itertools


def exclusions():
    rlst = []
    ord_directions = ['N ',
                      'E ',
                      'W ',
                      'S ']
    st_types = ['RD',
                'AV',
                'AVE',
                'ST',
                'BLVD',
                'BV',
                'DR',
                'CT',
                'PL',
                'PKY',
                'PKWY',
                'CIR']
    for ord in ord_directions:
        for st in st_types:
            rlst.append(ord + st)
    return rlst


def extract_street_names(text):
    """
    Extract street names from the given text.
    """
    # Remove directional words and parenthetical numbers
    text = re.sub(r'\b(ON|FROM|TO|Dead End)\b\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\([^)]*\)', '', text)
    
    # Define patterns to match street names
    patterns = [
        r'\b[NSEW]?\s*[A-Z]+(?:\s+[A-Z]+)*\s+(?:RD|AV|AVE?|ST|BLVD|BV|DR|CT|PL|PKY|PKWY|CIR)\b',
        r'\b[NSEW]?\s*\d+(?:ST|ND|RD|TH)?\s+(?:ST|PL)\b',
        r'\b[NSEW]?\s*AVENUE\s+[A-Z]\b'
    ]
    
    # Store all matches with their positions
    all_matches = []
    
    # Process each pattern and collect ALL matches
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            all_matches.append((match.start(), match.group().strip()))
    
    # Sort matches by position to maintain order
    all_matches.sort()
    
    # Process matches and handle duplicates
    streets = []
    seen = set()
    
    for _, street in all_matches:
        if street not in seen and len(street) > 1 and street:
            seen.add(street)
            if re.search(r'\s[NSEW]\s', street):
                parts = re.split(r'\s+(?=[NSEW]\s)', street)
                for part in parts:
                    if part.strip() and part.strip() not in seen and len(part.strip()) > 2:
                        seen.add(part.strip())
                        streets.append(convert_street_number_suffix(convert_street_abbreviation(part.strip())))
            else:
                streets.append(convert_street_number_suffix(convert_street_abbreviation(street)))
    
    return streets
def convert_street_number_suffix(street_name):
    """
    Convert street number suffix to the correct ordinal form.
    """
    def ordinal(n):
        """
        Convert an integer to its ordinal representation.
        """
        if 10 <= n % 100 <= 20:
            suffix = 'TH'
        else:
            suffix = {1: 'ST', 2: 'ND', 3: 'RD'}.get(n % 10, 'TH')
        return str(n) + suffix

    # Define a pattern to match the street number and type
    pattern = r'\b(\d+)\b'
    
    # Replace number suffixes with correct ordinal forms
    def replace(match):
        number = int(match.group(1))
        return ordinal(number)
    
    street_name = re.sub(pattern, replace, street_name)
    
    return street_name

def extract_single_addresses(text):
    """
    Extract full addresses from the given text.
    """
    # Define patterns to match full addresses
    patterns = [
        r'\b\d+\s+[NSEW]?\s*[A-Z]+(?:\s+[A-Z]+)*\s+(?:RD|AV|AVE?|ST|BLVD|BV|DR|CT|PL|PKY|PKWY|CIR|DR MARTIN LUTHER KING JR DR)\b'
    ]
    
    # Store all matches
    addresses = []
    
    # Process each pattern and collect all matches
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            addresses.append(match.group().strip())
    
    return addresses

def convert_street_abbreviation(street_name):
    """
    Convert street abbreviation to full form, ensuring no double replacements.
    """
    # Define a dictionary for abbreviation replacements
    replacements = {
        ' AV ': ' AVE ',
        ' AV': ' AVE'
    }
    
    # Replace abbreviations with full forms, ensuring no double replacements
    for abbr, full in replacements.items():
        if abbr in street_name and not street_name.endswith(full):
            street_name = street_name.replace(abbr, full)
    
    return street_name


if __name__ == "__main__":

    cwd = Path(os.getcwd())
    menu_money_fp = cwd / "data/menu_money.csv"
    json_fp = cwd / "data/streets.json"

    new_money_menu_fp = cwd / "data/new_menu_money.csv"

    with open(json_fp, 'r', encoding="utf-8") as jsonfile:
        streets = json.load(jsonfile)

    menu_money = load_csv(menu_money_fp)
    allstreets = list(set(streets.keys()))

    new_menu_money = []
    for row in menu_money:
        loc_string = row['description']
        row['addresses'] = extract_street_names(loc_string)
        if len(row) == 1:
            row['addresses'] = extract_single_addresses(loc_string)
        new_menu_money.append(row)

    fieldname = ['year',
                 'ward',
                 'cost',
                 'category',
                 'program',
                 'description',
                 'addresses']
    
    with open(new_money_menu_fp, 'w', encoding='utf-8') as newfile:
        csvwriter = csv.DictWriter(newfile, fieldnames=fieldname)
        csvwriter.writeheader()
        for row in new_menu_money:
            csvwriter.writerow(row)
