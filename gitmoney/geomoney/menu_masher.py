from .street_search import load_csv
from pathlib import Path
import os
import csv
import json
import re


def extract_street_names(text):
    """
    Extract street names from the given text.
    """
    # remove directional words and parenthetical numbers
    text = re.sub(r'\b(ON|FROM|TO|Dead End)\b\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\([^)]*\)', '', text)
    
    # define patterns to match street names
    patterns = [
        r'\b[NSEW]?\s*[A-Z]+(?:\s+[A-Z]+)*\s+(?:RD|AV|AVE?|ST|BLVD|BV|DR|CT|PL|PKY|PKWY|CIR)\b',
        r'\b[NSEW]?\s*\d+(?:ST|ND|RD|TH)?\s+(?:ST|PL)\b',
        r'\b[NSEW]?\s*AVENUE\s+[A-Z]\b'
    ]
    
    # store all matches with their positions
    all_matches = []
    
    # process each pattern and collect ALL matches
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            all_matches.append((match.start(), match.group().strip()))
    
    # sort matches by position to maintain order
    all_matches.sort()
    
    # process matches and handle duplicates
    streets = []
    seen = set()
    
    # process each match and extract street names
    for _, street in all_matches:
        if street not in seen and len(street) > 1 and street:

            # add street to seen set
            seen.add(street)

            # check if street contains a direction
            if re.search(r'\s[NSEW]\s', street):

                # split street into parts and process each part
                parts = re.split(r'\s+(?=[NSEW]\s)', street)

                # process each part and add to seen set
                for part in parts:

                    # check if part is not empty and not in seen set
                    if part.strip() and part.strip() not in seen and len(part.strip()) > 2:
                        # clean street name
                        cleaned_street = convert_street_number_suffix(convert_street_abbreviation(part))
                        if cleaned_street not in seen:
                            seen.add(cleaned_street)
                        # add cleaned street to streets list
                        streets.append(cleaned_street)
            

            else:
                # clean street name
                cleaned_street = convert_street_number_suffix(convert_street_abbreviation(street))
                # add cleaned street to seen set
                if cleaned_street not in seen:
                    seen.add(cleaned_street)
                # add cleaned street to streets list
                streets.append(cleaned_street)
    
    return streets


def convert_street_number_suffix(street_name):
    """
    Convert street number suffix to the correct ordinal form only for street names.

    For example, "1 ST" should be converted to "1ST".

    Args:
    street_name (str): The street name to process.

    Returns:
    str: The street name with the correct ordinal form for numbered streets.
    """
    # special pattern for numbered streets (where ST refers to STREET)
    numbered_street_pattern = r'\b(\d+)\s+(ST|PL)\b'
    
    # look up correct suffix for a given number
    def ordinal(n):
        """Convert an integer to its ordinal representation."""
        if 10 <= n % 100 <= 20:
            suffix = 'TH'
        else:
            suffix = {1: 'ST', 2: 'ND', 3: 'RD'}.get(n % 10, 'TH')
        return str(n) + suffix
    
    # replace function for numbered streets
    def numbered_replace(match):
        number = int(match.group(1))
        street_type = match.group(2)
        return ordinal(number) + " " + street_type
    
    # handle numbered streets
    result = re.sub(numbered_street_pattern, numbered_replace, street_name)
    
    return result
    

def extract_single_addresses(text):
    """
    Extract full addresses from the given text.
    """
    # define patterns to match full addresses
    patterns = [
        r'\b\d+\s+[NSEW]?\s*[A-Z]+(?:\s+[A-Z]+)*\s+(?:RD|AV|AVE?|ST|BLVD|BV|DR|CT|PL|PKY|PKWY|CIR|DR MARTIN LUTHER KING JR DR)\b'
    ]
    
    # store all matches
    addresses = []
    
    # process each pattern and collect all matches
    for pattern in patterns:
        for match in re.finditer(pattern, text):
            addresses.append(match.group().strip())
    return addresses


def convert_street_abbreviation(street_name):
    """
    Convert street abbreviation to full form, ensuring no double replacements.

    Args:
    street_name (str): The street name to process.

    Returns:
    str: The street name with all abbreviations replaced with full forms.
    """
    # define a dictionary for abbreviation replacements
    replacements = {
        r'\bAV\b': 'AVE'
    }
    
    # replace abbreviations with full forms, ensuring no double replacements
    for abbr, full in replacements.items():
        street_name = re.sub(abbr, full, street_name)
    
    return street_name


def main():
    # paths to the data files
    cwd = Path(os.getcwd())
    menu_money_fp = cwd / "gitmoney/data/menu_money.csv"
    json_fp = cwd / "gitmoney/data/streets.json"
    new_money_menu_fp = cwd / "gitmoney/data/new_menu_money.csv"
    menu_money = load_csv(menu_money_fp)

    # process the data
    new_menu_money = []
    for row in menu_money:
        loc_string = row['description']
        row['addresses'] = extract_street_names(loc_string)
        if len(row['addresses']) == 1:
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


if __name__ == "__main__":
    main()

