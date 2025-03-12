# **Menu Money** 
   
# **Welocme to Menu Money!**

# **Authors**
    Libby Seline 
    Riley Morrison
    Alex McMurtry 
    Getnet Dejene

1. **Abstract**
    The Menu Money project collects and analyzes Chicago datasets—specifically 
    311 service call data—alongside web-scraped data on aldermanic expenditures 
    from the "Menu" program, organized by district. GIS data on Menu program 
    expenditures has been extracted from the "Menu" program dataset. Data on 
    aldermen and their tenure has been scraped from Wikipedia. In addition to 
    aldermanic and Menu program data, 311 call records have been extracted from 
    the Chicago Data Portal via its API. The project aims to better understand 
    the relationship between Menu program expenditures and 311 service calls, 
    while also exploring whether these expenditures address constituents’ 
    concerns about their community, and provides data visualization to illustrate 
    these insights.

2. **Data Sources:**

    2.1 JakeJSmith's scraped Alder menu money database with GIS data: 
        https://github.com/jakejsmith/ChicagoMenuMoney/blob/main/data-dictionary.md

    2.2 Chicago Data Portal (API): 311 service call records
        https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/about_data

    3.3 Wikipedia List of Chicago Aldermen:
        https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923
      
3.  **How to run the project:**

gitmoney can be run using the following commands:

```
uv sync
uv run gitmoney/run_and_visualize.py -a
```

This will 

To overwrite existing data, or to run a specific part, please use the
following arguments:
<br>

'-a', '--all': to run the full program and overwrite all data <br>
'-g', '--geo': to run and overwrite the geomoney data files <br>
'-c', '--calls': to run and overwrite the 311 data files <br>
'-w', '--wiki': to run the scraper and overwrite wiki data files <br>
'-j', '--join': to join 311 calls and aldermanic data, overwrite data files <br>
'-r', '--ratio': to overwrite the ratio .html <br>
'-m', '--geomoney': to overwrite the geomoney map .html <br>

# Formal Methodology


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
