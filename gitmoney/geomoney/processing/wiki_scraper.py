import lxml.html
import httpx 
import pandas as pd
import re
import json
from lxml.cssselect import CSSSelector
import os
import pathlib
### Main Function ###

data_file = pathlib.Path(__file__).parent.parent / "data/"

def clean_join_wiki_data():
    """
    Main function to collect, join, and clean wikipedia data
    
    outputs: 
        alder_clean: clean dataset with each ward's alderperson between 
        2018 and 2023
    """
    all_alderpeople = join_table_bullets()
    alders_each_year = alders_fill_down(all_alderpeople)
    alder_clean = drop_rows_correct_2022(alders_each_year)
    
    alder_clean = alder_clean.sort_values(["Clean Ward", "filled_year"])
    
    alder_clean.to_csv(data_file/"all_alderpeople_2018_23.csv")
    
    return alder_clean

### Associated Functions ###

## If we were to separate this file into separate files I'd propose:##

## SECTION 1: WIKI SCRAPE ##

### Getnet Function ###
# Designed to grab & process table data

def scrape_wikipedia_tables(url):
    """
    Scrape data about Chicago alderpersons from tables in a Wikipedia page.

    This function extracts information about alderpersons for each ward in 
    Chicago from tables in a given Wikipedia URL. It collects data including 
    the ward number, alderperson name, start and end dates of their term, party 
    affiliation, and any additional notes.

    Args:
        url (str): The URL of the Wikipedia page to scrape.

    Returns:
        list: A list of dictionaries, where each dictionary contains information about
        an alderperson. The keys in each dictionary are:
        - "Ward": The ward number
        - "Alderperson": The name of the alderperson
        - "Start Date": The start date of their term
        - "End Date": The end date of their term (or "Present" if still in office)
        - "Party": The political party affiliation of the alderperson
        - "Notes": Any additional notes about the alderperson or their term
    """

    response = httpx.get(url)
    root = lxml.html.fromstring(response.content)
    
    all_data = []

    # Find all tables with class "wikitable sortable"
    tables = root.cssselect('table.wikitable.sortable')

    for table in tables:
        # Try to find the preceding h3 element for ward information
        ward_header = table.xpath('./preceding::h3[1]')
        if ward_header:
            ward_text = ward_header[0].text_content().strip()
            ward_number = ward_text.split()[0]  
        else:
            continue  # Skip if no ward header found

        # Define specific CSS selectors for each column
        alderperson_selector = CSSSelector('th[scope="row"] a')
        term_selector = CSSSelector('td:nth-of-type(4)')
        party_selector = CSSSelector('td:nth-of-type(5) a')
        notes_selector = CSSSelector('td:nth-of-type(6)')

        # Extract rows from the table
        rows = table.cssselect('tr:nth-of-type(n+2)')

        # Iterate through each row
        for row in rows:
            # Extract data using the defined CSS selectors
            alderperson = alderperson_selector(row)
            if not alderperson:
                continue
            alderperson = alderperson[0].text_content().strip()
            
            term = term_selector(row)
            if term:
                term_text = ' '.join(term[0].xpath('.//text()')).strip().\
                    replace('\n', ' ')
                term_parts = term_text.split('–')
                start_date = term_parts[0].strip()  # Get the start date
                end_date = term_parts[1].strip() if len(term_parts) > 1 \
                    else "Present"  # Get the end date
            else:
                start_date = end_date = 'N/A'

            party = party_selector(row)
            party = party[0].text_content().strip() if party else 'N/A'
            
            notes = notes_selector(row)
            notes_text = ' '.join(notes[0].xpath('.//text()')).strip().\
                replace('\n', ' ') if notes else 'N/A'

            row_data = {
                "Ward": ward_number,
                "Alderperson": alderperson,
                "Start Date": start_date,
                "End Date": end_date,
                "Party": party,
                "Notes": notes_text
            }

            # Append the data to the list
            all_data.append(row_data)

    return all_data

### Libby Functions ###
# Designed to Grab Bullet Points from Wikipedia

def compile_aldermen_for_wards(ul_element, ward_number, aldermen_dict):
    """
    Gather each the ward aldermen for wards whose aldermen are listed as bullet
    points. 
    
    inputs:
        ul_element: element known to contain bullet points
        ward_number: str associated with number of ward
        aldermen_dict: dictionary to contain ward_numbers as the key, values 
        will be a list of dictionaries. Key is an alderman's name, value is any 
        link associated with them
    
    outputs: 
        aldermen_dict: dictionary to contain ward_numbers as the key, values 
        will be a list of dictionaries. Key is an alderman's name, value is any 
        link associated with them
    
    """
    ward_aldermen = []
    bullet_points = ul_element.cssselect("li")
    for bullet in bullet_points:
        links = bullet.cssselect('a')
        profile_link = None        
        if links is not None:
            for element in links:
                # Wikipedia will often link to a file or its bibliography. I 
                # only want a link if it has the person's biography there
                href = element.get('href')
                if re.search("File", str(href), re.IGNORECASE) or \
                    re.search("cite_note", str(href), re.IGNORECASE):
                    continue
                else:
                    profile_link = "https://en.wikipedia.org/" + href
                    break
        # Now I should create a dictionary with the indivudual as the key and 
        # the links as the value
        # I will then add this dictionary to a list. This list will then be the 
        # value of final dictionary where the key is the ward
        
# clean name courtesy of: 
# https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
        clean_name = re.sub(r'\([^)]*\)', '', bullet.text_content())
        person_tuple = (str.strip(clean_name), profile_link)
        ward_aldermen.append(person_tuple)
    
    aldermen_dict[ward_number] = ward_aldermen
    
    return aldermen_dict

def find_ward(url):
    """
    Create a dictionary with each a ward, each alderperson, and a link to their 
    webpage if available. 
    
    inputs: None
    
    outputs: 
        aldermen_dict: dictionary to contain ward_numbers as the key, values 
        will be a list of dictionaries. Key is an alderman's name, value is any 
        link associated with them
    
    """

    aldermen_dict = {}
    url_text = httpx.get(url)
    root = lxml.html.fromstring(url_text.text)

    body_content = root.cssselect('div.mw-body-content')[0]
    heading = body_content.cssselect('div.mw-heading.mw-heading3')

    for ward_number in heading:
        num = re.findall("\\d+", ward_number.text_content())
        ward = num[0]
        
        # Each part of the page is structured a bit differently. 
        # Sometimes, I a ul element is found immediately after the heading. Other 
        # times, they have figures or paragraphs after the heading and before the 
        # list of aldermen. For that reason, I grab the next five elements.
        
        sibling_1 = ward_number.getnext()
        sibling_2 = sibling_1.getnext()
        sibling_3 = sibling_2.getnext()
        sibling_4 = sibling_3.getnext()
        sibling_5 = sibling_4.getnext()
        
        for element in [sibling_1, sibling_2, sibling_3, sibling_4, sibling_5]:
            if re.search("table", str(element), re.IGNORECASE):
                # if there's a table associated with this ward, I don't care about
                # it, so I move onto the next ward
                break
            elif re.search("ul", str(element), re.IGNORECASE):
                aldermen_dict = \
                    compile_aldermen_for_wards(element, ward, aldermen_dict)
                break
            else:
                continue

    return aldermen_dict
        
def find_alder_link(aldermen_dict):
    """
    Use the aldermen_dict to go to available websites and grab the dates the 
    alderperson served. Return a dictionary where the key is the ward, and the 
    value is list of tuples. Each tuple contains the alderperson's name and 
    their dates. 
    
    inputs: 
        aldermen_dict: dictionary to contain ward_numbers as the key, values 
        will be a list of dictionaries. Key is an alderman's name, value is any 
        link associated with them
    
    outputs: 
        aldermen_date_dict = a dictionary where the key is the ward, and the 
    value is list of tuples. Each tuple contains the alderperson's name and 
    their dates. 
    
    """
    
    aldermen_dates_dict = {}
    for ward, aldermen_and_links in aldermen_dict.items():
        all_info = []
        for tup in aldermen_and_links:
            alderperson = tup[0]
            link = tup[1]
            # we have a series of different labels for dates so we can evaluate 
            # what has happened
            if link is not None:
                dates = "link exists"
                resp = httpx.get(link)
                if resp.status_code == 200:
                    root = lxml.html.fromstring(resp.text)
                    # This is the box that has the in office dates, but sometimes 
                    # it doesn't exist
                    info_box = root.cssselect("table.infobox.vcard")
                    if len(info_box) == 1:
                        info_elements = info_box[0].cssselect('th.infobox-header')
                        if len(info_elements) == 0:
                            dates = "no headings"
                        else:
                            for element in info_elements:
                                # we want to find the row header that is associated 
                                # with being a Chicago alderperson — and not the 
                                # council president                             
                                if re.search("ward", element.text_content(), \
                                    re.IGNORECASE) or re.search("alder", \
                                    element.text_content(), re.IGNORECASE) or \
                                    re.search("Chicago City Council", \
                                    element.text_content(), re.IGNORECASE) and \
                                    not re.search("President", \
                                        element.text_content(), re.IGNORECASE):
                                    # We also want to see if they have the correct
                                    # ward listed -- if there is one. 
                                    if re.search("\\d+", element.text_content(), 
                                            re.IGNORECASE) is None or ward in \
                                                element.text_content():
                                    # We want to find the row itself this is 
                                    # associated  with rather than the actual header     
                                        row_parent = element.getparent()
                                    # The header we want is in the next two rows
                                        header_option1 = row_parent.getnext()
                                        header_option2 = header_option1.getnext()
                                        if re.search("office", \
                                            header_option1.text_content(), \
                                                re.IGNORECASE):
                                            dates_raw = header_option1.text_content()
                                            dates_raw = re.sub("In office", "", \
                                                dates_raw)
                                            dates_raw = re.sub("Assumed office", \
                                                "", dates_raw)
        # clean name courtesy of: 
        # https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
                                            dates_raw = re.sub(r'\([^)]*\)', ' ', \
                                                dates_raw)
                                            dates_raw = re.sub(r'\xa0', ' ', \
                                                dates_raw)
                                            dates = str.strip(re.sub(r'\[[^)]*\]', \
                                                ' ', dates_raw))
                                        elif re.search("office", \
                                        header_option2.text_content(), re.IGNORECASE):
                                            dates_raw = header_option2.text_content()
                                            dates_raw = re.sub("In office", "", \
                                                dates_raw)
                                            dates_raw = re.sub("Assumed office", \
                                                "", dates_raw)
        # clean name courtesy of: 
        # https://stackoverflow.com/questions/640001/how-can-i-remove-text-within-parentheses-with-a-regex
                                            dates_raw = re.sub(r'\([^)]*\)', \
                                                ' ', dates_raw)
                                            dates_raw = re.sub(r'\xa0', ' ', \
                                                dates_raw)
                                            dates = str.strip(re.sub(r'\[[^)]*\]', \
                                                '', dates_raw))
                                        else:
                                            dates = "unknown from link"
                                        break
                                else:
                                    dates = "no suitable heading"
                    else:
                        dates = "ERROR, BOX ELEMENT"
                    
                else:
                    dates = "ERROR, BAD LINK"       
            else:
                dates = "Unknown"
                
            person_tup = (alderperson, dates)
            all_info.append(person_tup)
            
        aldermen_dates_dict[ward] = all_info
            
    return aldermen_dates_dict

def aldermen_and_dates(aldermen_dates_dict):
    """
    Clean up the dates listed with each alderperson in aldermen_dates_dict. 
    Put into a new dictionary that contains ward, alderperson, start date, 
    end date, party, and notes.
    
    inputs:    
        aldermen_date_dict: a dictionary where the key is the ward, and the 
    value is list of tuples. Each tuple contains the alderperson's name and 
    their dates. 
    
    outputs: 
    list: A list of dictionaries, where each dictionary contains information about
        an alderperson. The keys in each dictionary are:
        - "Ward": The ward number
        - "Alderperson": The name of the alderperson
        - "Start Date": The start date of their term
        - "End Date": The end date of their term (or "Present" if still in office)
        - "Party": The political party affiliation of the alderperson
        - "Notes": Any additional notes about the alderperson or their term
    """
    
    all_data = []
    alderman_and_dates = {}

    for ward, values in aldermen_dates_dict.items():
        aldermen = []
        for alder_info in values:
            alderperson = alder_info[0]
            dates = alder_info[1]
            if re.search("\\d+", dates):
                # Two types of hyphens I have to be aware of here
                if re.search('–', dates):
                    beg_end = re.split('–', dates)
                    begin = beg_end[0]
                elif re.search('-', dates):
                    beg_end = re.split('-', dates)
                    begin = beg_end[0]
                else:
                    beg_end = []
                    begin = dates
                if len(beg_end) == 2:
                    end = beg_end[1]
                else:
                    end = "present"
                    
    # To ensure I'll match Getnet's data, I'll copy the format he used
                row_data = {
                    "Ward": ward,
                    "Alderperson": alderperson,
                    "Start Date": str.strip(begin),
                    "End Date": str.strip(end),
                    "Party": None,
                    "Notes": None
                }
                all_data.append(row_data)
                    
            else:
                continue
            
    return all_data

## SECTION 2: WIKI CLEAN ##

def alders_fill_down(all_alderpeople):
    """
    Create a dataframe that has a row for each year an alderperson served.
    
    Inputs:
        all_alderpeople: (Pandas Dataframe), every alderperson collected and 
        information about their term
    
    Outputs:
        alder_each_year: (Pandas Dataframe), every alderperson with an entry 
        for each year they served
    """
    
    # Create Clean Columns
    
    all_alderpeople["Clean Ward"] = \
        all_alderpeople["Ward"].str.extract('(\\d+)')
    all_alderpeople["Start Year"] = \
        all_alderpeople["Start Date"].str.extract('(\\d{4})')
    all_alderpeople["End Year"] =  \
        all_alderpeople["End Date"].str.extract('(\\d{4})')
    all_alderpeople["Start Year"] =  \
        pd.to_numeric(all_alderpeople['Start Year'])
    all_alderpeople["End Year"] =  pd.to_numeric(all_alderpeople['End Year'])

    # Create a column based on End Year. We will now create a row with identical 
    # information for each alderperson, but a unique year in the "End Year for
    # Fill" column, which will have one entry for year served
    
    all_alderpeople["filled_year"] =  all_alderpeople["End Year"]
    all_alderpeople["filled_year"] =  \
        all_alderpeople["filled_year"].fillna(2023)
        
    # This dataset serves as a placeholder. We will omit the first row later on    
    alder_each_year = all_alderpeople[0:1]

    for index, row in all_alderpeople.iterrows():
        start = int(row["Start Year"])
        end = int(row["filled_year"])
        for year in range(start, end + 1): 
            new_row = pd.DataFrame([{'Ward': row["Ward"], \
                'Alderperson': row["Alderperson"], \
                'Start Date': row["Start Date"],
                'End Date': row["End Date"],
                'Party': row["Party"],
                'Notes': row["Notes"],
                'Clean Ward': int(row["Clean Ward"]),
                'Start Year': row["Start Year"],
                'End Year': row["End Year"],
                'filled_year': int(year),
                }])
            
            alder_each_year = pd.concat([alder_each_year, new_row], \
                ignore_index=True)
            
    alder_each_year = alder_each_year[1::]
    return alder_each_year.reset_index(drop=True)

def drop_rows_correct_2022(alder_each_year):
    """
    Drop rows representing serviced before the year 2018. Add in an alderperson 
    not included on Wikipedia
    
    Inputs:
        alder_each_year: (Pandas Dataframe), every alderperson with an entry 
        for each year they served
        
    Outputs:
        alder_clean: (Pandas Dataframe), every row has one alderperson and a 
        year corresponding with an entry between 2018 and 2023. Each ward will 
        have 6 entries, resulting in 50 rows
    """
    
    # Drop rows with entries before 2018
    alders_2018_2023 =  \
        alder_each_year.loc[(alder_each_year['filled_year'] >= 2018)]

    alders_2018_2023.reset_index(drop= True)
    alders_2018_2023.drop_duplicates(ignore_index= True)
    
    # To correct for a single missing alderperson, I add them in here
    
    ward_24_corection1 = pd.DataFrame([{'Ward': 24, \
            'Alderperson': "Monique Scott", \
            'Start Date': "June 22, 2022",
            'End Date': "present",
            'Party': "",
            'Notes': "",
            'Clean Ward': 24,
            'Start Year': 2022,
            'End Year': None,
            'filled_year': float(2022),
            }])

    ward_24_corection2 = pd.DataFrame([{'Ward': "24", \
            'Alderperson': "Monique Scott", \
            'Start Date': "June 22, 2022",
            'End Date': "present",
            'Party': "",
            'Notes': "",
            'Clean Ward': 24,
            'Start Year': "2022",
            'End Year': None,
            'filled_year': float(2023),
            }])

    alders_2018_2023_fix = pd.concat([alders_2018_2023, ward_24_corection1, \
        ward_24_corection2], ignore_index=True)    
    # Find rows where wards have two entries for a year
    
    year_count = alders_2018_2023_fix.groupby(["Clean Ward","filled_year"])\
        .size().rename("count_by_year").reset_index()

    year_count_over = year_count.loc[(year_count['count_by_year'] > 1)]
    year_count_one = year_count.loc[(year_count['count_by_year'] == 1)]
    
    # Find wards and years with more than two entries. Only keep the first entry
    
    two_entries = pd.merge(alders_2018_2023_fix, year_count_over, \
        on=["Clean Ward", "filled_year"])
    two_entries = two_entries.\
        drop_duplicates(subset=['Clean Ward', 'filled_year'], keep = 'last')
    two_entries = two_entries.drop(columns= 'count_by_year')
    
    # Find wards with only one entry
    one_entry = pd.merge(alders_2018_2023_fix, year_count_one, \
        on=["Clean Ward", "filled_year"])
    one_entry = one_entry.drop(columns= 'count_by_year')
    
    # Join the cleaned up datasets of "one_entry" and "two_entry"
    
    alder_clean = pd.concat([two_entries, one_entry], ignore_index=True)
    
    return alder_clean


## SECTION 3: WIKI JOIN ##
### Implementing above bunctions to prepare for join ###

def gather_tables(url):
    """
    Scrape tables from Wikipedia
    
    Inputs:
        - "url": (str), link to Wikipedia page of alderpeople
    
    Returns:
        list: A list of dictionaries, where each dictionary contains information about
        an alderperson. The keys in each dictionary are:
        - "Ward": The ward number
        - "Alderperson": The name of the alderperson
        - "Start Date": The start date of their term
        - "End Date": The end date of their term (or "Present" if still in office)
        - "Party": The political party affiliation of the alderperson
        - "Notes": Any additional notes about the alderperson or their term
    """
    
    # Call the function and store the scraped data
    scraped_data = scrape_wikipedia_tables(url)
    
    return scraped_data

def gather_bullets(url):
    """
    Scrape bullets from Wikipedia
    
    Inputs:
        - "url": (str), link to Wikipedia page of alderpeople
    
    Returns:
        list: A list of dictionaries, where each dictionary contains information 
        about an alderperson. The keys in each dictionary are:
        - "Ward": The ward number
        - "Alderperson": The name of the alderperson
        - "Start Date": The start date of their term
        - "End Date": The end date of their term (or "Present" if still in office)
        - "Party": The political party affiliation of the alderperson
        - "Notes": Any additional notes about the alderperson or their term
    """
    
    alderperson_dict = find_ward(url)
    alder_dates = find_alder_link(alderperson_dict)
    bullet_data = aldermen_and_dates(alder_dates)
    
    return bullet_data

### Join Function ###

def join_table_bullets():
    """
    Concaenate two lists of dictionaries together and use them to create a 
    database of alderpeople in Chicago. 
    
    outputs:
        all_alderpeople: (Pandas Dataframe), every alderperson collected and 
        information about their term
    """
    url = 'https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923'
    full_wards = []
    
    scraped_tables = gather_tables(url)
    scraped_bullets = gather_bullets(url)
    
    full_wards.extend(scraped_tables)
    full_wards.extend(scraped_bullets)
            
    all_alderpeople = pd.DataFrame(full_wards)
    
    
    return all_alderpeople
            

