import os
import pathlib
import sys
sys.path.insert(1, 'processing')
import wiki_scraper as wiki
import httpx


url = 'https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923'


def test_scrape_wikipedia_tables(url):

    # Make an HTTP request
    response = httpx.get(url)
    assert response.status_code == 200, f"Failed to fetch the Wikipedia page. Status code: {response.status_code}"

    # Call the function 
    results = wiki.scrape_wikipedia_tables(url)

    # Verify the structure of the returned data
    expected_keys = {"Ward", "Alderperson", "Start Date", "End Date", "Party", "Notes"}
    for row in results:
        assert isinstance(row, dict), "Each item in the list should be a dictionary."
        assert set(row.keys()) == expected_keys, f"Unexpected keys in the dictionary: {row.keys()}"

def test_find_alder_link():
    resp= httpx.get(url)
    assert resp.status_code == 200, f"Failed to fetch the Wikipedia page. \
        Status code: {resp.status_code}"
    
    aldermen_dict = wiki.find_ward(url)
    dates_dict = wiki.find_alder_link(aldermen_dict)
    
    for ward, list_of_tuples in dates_dict.items():
        for tup in list_of_tuples:
            if tup[1] == "link exists":
                raise NotImplementedError(f"Date or error does not \
                    appear with {tup[0]}")    
    

def test_clean_join_wiki_data():
    alder_data = wiki.clean_join_wiki_data()
    years = alder_data.groupby(['filled_year']).size().reset_index()
    wards = alder_data.groupby(['Clean Ward']).size().reset_index()
    
    assert len(alder_data) == 300, f"There are {len(alder_data)} \
        in your data. Not 300"
    assert len(years) == 6,  f"There are {len(years)} \
        in your data. Not 6"
    assert len(wards) == 50,  f"There are {len(wards)} \
        in your data. Not 50"
