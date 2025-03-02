import json
import lxml.html
import httpx
from lxml.cssselect import CSSSelector

url = 'https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923'

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
                term_text = ' '.join(term[0].xpath('.//text()')).strip().replace('\n', ' ')
                term_parts = term_text.split('–')
                start_date = term_parts[0].strip()  # Get the start date
                end_date = term_parts[1].strip() if len(term_parts) > 1 else "Present"  # Get the end date
            else:
                start_date = end_date = 'N/A'

            party = party_selector(row)
            party = party[0].text_content().strip() if party else 'N/A'
            
            notes = notes_selector(row)
            notes_text = ' '.join(notes[0].xpath('.//text()')).strip().replace('\n', ' ') if notes else 'N/A'

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

    # Save the data to a JSON file
    with open('getnet_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    return all_data

# Call the function and store the scraped data
scraped_data = scrape_wikipedia_tables(url)
