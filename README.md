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
    aldermanic and Menu money data, 311 call records have been extracted from 
    the Chicago Data Portal via its API. The project aims to better understand 
    the relationship between Menu program expenditures and 311 service calls 
    while providing data visualization to illustrate these insights.

2. **Data Sources:**

    2.1  JakeJSmith's scraped Alder menu money database with GIS data: 
        https://github.com/jakejsmith/ChicagoMenuMoney/blob/main/data-dictionary.md

    2.2 Chicago Data Portal (API): 311 service call records
        https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/about_data

    3.3 Wikipedia List of Chicago Aldermen:
        https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923
      
3.  **How to run the project:**

All of subfunctions of gitmoney can be run using the following command:

"uv run gitmoney/run_and_visualize.py -a".

To overwrite existing data, or to run a specific part, please use the
following arguments:


'-a', '--all': to run the full program and overwrite all data
'-g', '--geo': to run and overwrite the geomoney data files
'-c', '--calls': to run and overwrite the 311 data files
'-w', '--wiki': to run the scraper and overwrite wiki data files
'-j', '--join': to join 311 calls and aldermanic data, overwrite data files
'-r', '--ratio': to overwrite the ratio .html
'-g', '--geomoney': to overwrite the geomoney map .html

## Tools
* R/RStudio
* R packages
> * tidyverse:  for data manipulation
> * janitor: for cleaning
> * readxl: for working with Excel files
> * skimr # for initially understanding data -- > skim function

Run this code in the R Console to install packages
```
install.packages(c("tidyverse", "janitor", "readxl", "skimr"))
```
## Files
What are they? 

# Formal Methodology

# Kudos
