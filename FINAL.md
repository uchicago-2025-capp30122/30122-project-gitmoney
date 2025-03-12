## ** Video Summary (Getnet, Alex, Riley) **
https://uchicago.box.com/s/04p3aq6gku4vwgymp0z1cjawiq98oq5n

## ** Data Documentation **

# Sources

311
    - Description: Records for every non-emergency call made to Chicago’s 311 line for assistance. Each row is a call, and has time, date, location, ward and category data.

    - Gaps: There weren’t any categories that could be reasonably connected with some of our Menu Money categories, like Schools and Libraries. That’s not to say no 311 calls had to do with schools or libraries, they just weren’t coded that way.

    - Challenges: It was a challenge using an API to download this data, because the API used an O(N) algorithm to access data, so the further back it pulled data, the slower it became. This wasn’t immediately apparent, and I tried a bunch of different techniques to get it to work (OAuth keys, timeout error management and asking it to run again). Fortunately, the data portal offered a bulk download with csv, which we used instead. It was also a challenge to map the 311 categories to the menu money categories, which didn’t fit perfectly.

Wiki
    - Description: For our project, we scraped Wikipedia to collect alderperson data for each ward. The data is organized into both tables and paragraphs. We gathered and categorized relevant alderperson information for each ward, including ward number, alderperson name, start and end dates, party affiliation, and additional notes. 

    - Gaps: Although the website provides alderperson data dating back to 1923, it is incomplete in some areas, particularly for certain wards. As a result, we need to manually add missing data into our code to complete the dataset.

    - Challenges: The primary challenge we faced was cleaning the scraped data. While we could have explored alternative data sources for alderperson information for each ward, doing so would have been challenging and could have impacted our project timeline. As a result, we decided to use Wikipedia’s alderperson data, as it was more efficient and would not significantly affect the overall progress of our project.

Menu Money
    - Description: Jake J Smith’s scraped Alder menu money database (csv). It contains a row for every project that alderpeople spent their menu money funds on each year. It has columns for project category, year, ward and some string based location information for streets where the project occurred.
    
    - Gaps: For many of the projects, the funding quantity is 0. We’re relatively sure this just means that the project is ongoing from last year, but that no new funds have been allocated to it. However, we’re not certain and these $0 rows are still in our dataset, which might cloud the interpretation of average cost or median cost calculations. Additionally, we have not added logic to include “middle” street segments for projects that extend beyond the block at either end of the project. So if a project description occurs along four block segments, we only include the street segments at either end.

    Challenges: One huge challenge for our map visualization was turning the menu money string location data into line segments on a map. It required a ton of regex work and GIS triangulation to convert these strings into lines. 

## ** Dataflows and Structure **

The data moved downward through these steps

1. Capturing the data:
    
    CSV download: 311 (csv lives in this box link - https:\\uchicago.box.com\s\dvijaxjxx9plkth729ftmb2ge5ebdbqt. To use it, download it from this folder, and put it in the data folder in the our gitmoney folder), menumoney (csv lives in our repository)
    
    Scraping: wiki alderperson data (using wiki_scraper.py in the processing folder)

2. Cleaning the data:
    
    Process_311_and_menu_money.py cleans and processes the 311 and menu money data
    
    Wiki_scraper.py cleans and processes the wiki data
    
    geomoney\menu_masher.py extracts street name, direction, and type from the text “description” data in the Menu Money dataset (data\menu_money.csv). It creates a new csv file (data\new_menu_money.csv). 
    
    geomoney\street_search.py takes the extracted street data and searches data from the Chicago streets shapefile (data\shapefiles\trans.shp). This shapefile is converted to a dictionary in which street name, direction, and type indexes all street segments associated with that street (data\streets.json). Finally, it combines information from data\new_menu_money.csv and streets.json to create data\final_menu_money.csv, which is merged with aldermanic and 311 data and contains the final combined menu money and street data. 

3. Joining the data
    
    process_311_and_menu_money.py joins 311 and menu money data into one csv - calls_money.csv

    join_alder_311_menudata.py joins the calls_money.csv and "all_alderpeople_2018_23.csv" datasets into “calls_money_pivot_with_alder.csv”

4. Visualizing the data
    
    chart.py, projects_per_ward.py and ratio.py create html visualizations, which they export into the charts folder, within the visualizations folder

    geomoney\data_visualization.py writes the street segment data for each Menu Money project to a pydeck object to provide an interactive visualization. The pydeck data is written to visualizations\charts\gitmoney_map.html

5. Command line functionality + final visualization
    
    run_and_visualize.py runs all of the above programs and composes them in a single explanatory HTML page, which it then opens in the users web browser when they enter the command

For an in depth look at each of our files, see the attached link - https://docs.google.com/spreadsheets/d/1yi3UXYMv0_f-hUMcc4xABlwmBV-wJE8N-mQQlZDRuqU/edit?gid=0#gid=0


## ** Team responsibilities **

Libby
- Scraping wiki alderperson data
- joining wiki alderperson data
- Creating exploratory calls and spending charts
- HTML analysis blurbs

Getnet
- Scraping wiki alderperson data
- Creating exploratory calls and spending charts
- Creating the HTML presentation 

Alex
- Extracting and mapping menu money description strings to GIS line segments. 
- Creating an interactive map visualization of menu money
- Creating the command line visualization program

Riley
- 311 scraping (until we pivoted to just using a csv)
- Cleaning / joining 311 and menu money datasets
- Creating the scatterplot
- HTML analysis blurbs

## ** Final thoughts **

Our project set out to better understand menu money project spending and city contract data. We wanted to know if there was any sign of corruption in the aldermanic spending patterns on menu money projects - certain companies or individuals getting repeat business from the same alder person over the years, perhaps with little to show for it.

We quickly figured out that contract data was going to be difficult to work with, and weren’t sure whether we could turn the menu money location strings into trackable\mappable data. So, we pivoted to 311 calls and decided to pursue a project focused on whether the spending projects that alder people pursued reflected the concerns that constituents raised about infrastructure in their calls.

We certainly explored these ideas and became much more familiar with the menu money spending and calls categories associated with infrastructure. We showed that 311 call trends have fallen significantly over the past 5 years, while categories of calls, categories of spending and number of projects have remained consistent. We also built a beautiful visualization for anyone who wants to see where menu money funds have been spent throughout the city.

However, a big weakness in our analysis is that menu money is only a small piece of the funding that alderpeople control. Who’s to say they aren’t responsive to their constituent concerns in other avenues? It’s not exactly fair for us to say that a ward is underfunding beautification, when perhaps all those projects just come from another (non-menu money) pot.
