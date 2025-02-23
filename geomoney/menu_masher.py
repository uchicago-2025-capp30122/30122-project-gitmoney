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

    """
    # Remove directional words and parenthetical numbers
    text = re.sub(r'\b(ON|FROM|TO|Dead End)\b\s*',
                  '',
                  text,
                  flags=re.IGNORECASE)
    text = re.sub(r'\([^)]*\)', '', text)
    exclusion_list = exclusions()
    patterns = [
        (r'[NSEW]\s+'                    # Direction prefix
        r'[A-Z]+(?:\s+[A-Z]+)*'         # Street name words
        r'\s+(?:RD|AV|AVE?|ST|BLVD|BV|DR|CT|PL|PKY|PKWY|CIR)'),

        (r'[NSEW]\s+'                    # Direction prefix
        r'(?:\d+(?:ST|ND|RD|TH)?\s+)'   # 1-3 digit number with optional 
        r'(?:ST|PL)'),                  # Street or Place suffix
        
        (r'[NSEW]\s+AVENUE\s+[A-Z]\b')
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
                    if part.strip() and part.strip() not in seen:
                        seen.add(part.strip())
                        if part not in exclusion_list:
                            streets.append(part.strip())
            else:
                streets.append(street)
    
    return streets


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
