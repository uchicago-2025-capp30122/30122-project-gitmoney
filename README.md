# **Menu Money** 
**Updated March 20, 2025**
   
# **Authors**
Libby Seline <br>
Riley Morrison <br>
Alex McMurtry <br>
Getnet Dejene <br>

# Abstract <br>
The Menu Money project collects and analyzes Chicago datasets—specifically 311 service call data—alongside web-scraped data on aldermanic expenditures from the "Menu" program, organized by district. GIS data on Menu program expenditures has been extracted from the "Menu" program dataset. Data on aldermen and their tenure has been scraped from Wikipedia. In addition to aldermanic and Menu program data, 311 call records have been extracted from the Chicago Data Portal. The project aims to better understand the relationship between Menu program expenditures and 311 service calls, while also exploring whether these expenditures address constituents’ concerns about their community, and provides data visualization to illustrate these insights.

More thorough report and video explanation of project can be found in [FINAL.md](https://github.com/uchicago-2025-capp30122/30122-project-gitmoney/blob/main/FINAL.md)

# Data Sources

1. JakeJSmith's scraped Alder menu money database with GIS data: 
        https://github.com/jakejsmith/ChicagoMenuMoney/blob/main/data-dictionary.md

2. Chicago Data Portal: 311 service call records
        https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/about_data

3. Wikipedia List of Chicago Aldermen:
        https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923

For an indepth look at project structure, check this [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1yi3UXYMv0_f-hUMcc4xABlwmBV-wJE8N-mQQlZDRuqU/edit?gid=0#gid=0)
      
# How to run the project
## Step 1: Download Data
To run this project, you will need to download our 311 data, which can be found here.  
here: https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/about_data. <br>
<br>
Move the data into the gitmoney/data/raw_csvs folder. From there, you should be able to run 'gitmoney.'

## Step 2: Run Program
gitmoney can be run using the following commands:

```
uv sync
uv run python -m gitmoney -a
```

To overwrite existing data, or to run a specific part, please use the following arguments:
<br>

'-a', '--all': to run the full program and overwrite all data <br>
'-g', '--geo': to run and overwrite the geomoney data files <br>
'-c', '--calls': to run and overwrite the 311 data files <br>
'-w', '--wiki': to run the scraper and overwrite wiki data files <br>
'-j', '--join': to join 311 calls and aldermanic data, overwrite data files <br>
'-r', '--ratio': to overwrite the ratio .html <br>
'-m', '--geomoney': to overwrite the geomoney map .html <br>
<br>

## Test
To test the project, run the following command
```
uv run pytest
```

Or test individual aspects with
```
uv run tests/test_311_menu_money_clean_merge.py
uv run tests/test_geomoney.py
uv run tests/test_join_alder_311.py
uv run tests/test_wiki_scraper.py
```

# Formal Methodology

## Wiki
To find alderpeople, we extracted the names from a wikipedia page. If available, we collected names and dates from tables on the page. If unavailable, we retrieved the names of alderpeople by scraping the bulletpoints and going to the personal wikipedia page associated with the link. This worked for all but one alderperson between 2018 and 2023. That person is manually entered into the data. 

## 311


## Geomoney
To extract streets data, we used regular expressions to extract street
direction, street name, and street type from the "description" field. 
For streets that only return one result, we also extract block number
information.

The vast majority of entries in the data follow one of four formats:

Single address: "317 S CAMPBELL AVE"

Two addresses (intersection): "W ROOSEVELT RD & S WOOD ST"

Three addresses (block): Example "ON ROOSEVELT FROM S LOOMIS ST (1400 W) TO S
ASHLAND AV (1600 W)" (note: our code does not yet include the logic to include
connecting segments between the first and last block segment)

Four address (blocks bound by intersections): "E 47TH ST & E 47TH PL &
S DREXEL BLVD & S COTTAGE GROVE AVE"

To match segments, we used the trans.shp file of all street segments in 
Chicago to create dictionaries indexed by street names. This creates a
dictionary that contains every segment named "S COTTAGE GROVE AVE" in Chicago,
for example. By searching each street for cross streets ("F_CROSS","T_CROSS"),
we are able to mark out blocks and intersections bounding each project. 

# Kudos

Thank you James and CAPP 122 TAs! Couldn't have come this far without you!
