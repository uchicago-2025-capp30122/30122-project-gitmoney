import httpx
import processing.wiki_scraper as wiki

url = 'https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923'


def test_scrape_wikipedia_tables(url):
    ## Teme, write a test to ensure data is fetched correctly
    pass

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
