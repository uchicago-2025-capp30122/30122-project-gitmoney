import pytest
import processing.wiki_scraper as wiki
import httpx
from processing.wiki_scraper import scrape_wikipedia_tables


url = 'https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923'

def test_scrape_wikipedia_tables():
    # Make an HTTP request
    response = httpx.get(url)
    assert response.status_code == 200, f"Failed to fetch the Wikipedia page. Status code: {response.status_code}"

    # Call the function
    results = scrape_wikipedia_tables(url)

    # Verify the content of the returned data
    assert len(results) > 0, "No data was scraped from the Wikipedia page."
    for row in results:
        assert isinstance(row["Ward"], str), "Ward should be a string."
        assert isinstance(row["Alderperson"], str), "Alderperson should be a string."
        assert isinstance(row["Start Date"], str), "Start Date should be a string."
        assert isinstance(row["End Date"], str), "End Date should be a string."
        assert isinstance(row["Party"], str), "Party should be a string."
        assert isinstance(row["Notes"], str), "Notes should be a string."


def test_find_alder_link():
    resp= httpx.get(url)
    assert resp.status_code == 200
    
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
    
    assert len(alder_data) == 300
    assert len(years) == 6
    assert len(wards) == 50
    
