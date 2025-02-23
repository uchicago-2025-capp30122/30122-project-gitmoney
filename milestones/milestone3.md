# What You Want to Know

As you may recall, our project is based on three datasets: 1) 311 data 2) Menu Money Data 3) Wikipedia's alderperson data.

While we intended to present a fully joined dataset today, we each discovered flaws in our pre-assigned datasets that prevented us from creating a fully joined dataset.

## 311 Data Complications
Riley put together an awesome API retrieval script! But the data unfortunately captured information from 2025. He intends on revisiting it this week so we can join the dataset soon. 

## Wikipedia Data Complications
Getnet and Libby scraped wikipedia! There were some small flaws in our individual scraping efforts, and we worked together to resolve them. A joined dataset of aldermen between 2012 and 2023 is in [data/wiki/alders_2012_2023.csv](https://github.com/uchicago-2025-capp30122/30122-project-gitmoney/blob/main/data/wiki/alders_2012_2023.csv). Libby is currently writing a little something to check that we can account for an alderperson for every year of interest. But she misses R so much and wishes pandas were as intuitive to her. 

## Menu Money
In terms of geolocating data, we are successfully extracting addresses from the
menu_money dataset. The data has a few different formats for which we need to 
account. The first is when no street is extracted. We can do little about this, 
but this actually makes up a small amount of the data. When one entity is 
extracted, we will need to extract the full address. When two entities are 
extracted, we can use the intersection based on the cross streets. Three entities
have the form ON <main street> FROM <cross1> TO <cross2>, which will make it easy
pinpoint the block. Finally we have four entities extracted, which are the 
bounding intersections. Given this, we are close to being able to fully link
the menu money data to the Chicago streets shapefile data at the block level.

# What's below? 

After joining, we will then query data to ask questions that will fuel our visualizations. These are the questions we have for the data, how we plan to query them, and a **rough** idea of visualizations that could alongside it. 

# GOALS
Visualizing problem areas, where people have concerns

**WHO** — Alderpeople, Chicago Citizens <br>
**WHAT** — 311 Calls (see categories), Menu Money Projects (see categories) <br>
**WHEN** — year (2012-2023) <br>
**WHERE** — (Lat, long) for 311 coords, project coordinates; ward shape <br>
**WHY** — government accountability, highlight need versus solutions enacted <br>
<br>
# Key Questions
**What 311 call is the most prevalent in the ward?**
_Query_: group by (ward), group by (year) summarize (calls) 
Viz for ward:
* Stacked Bar chart: 
  * X = year
  * Y = # of calls
  * Colors = cats
* Stacked Bar chart:
  * X = ward
  * Y = # of calls
  * Colors = cats
* Stacked Bar chart:
  * X = year
  * Y = $ spent
  * Colors = cats
* Stacked Bar chart:
  * X = ward
  * Y = $ spent
  * Colors = cats

**What category of menu money spending is most prevalent?**
_Query_: group by (category, year) summarize (project cost, (count(total projects))

**What’s the average cost of a project per category? Per ward?**
_Query_: group by (category, year) MEAN (project cost) 

**How many projects are funded every year PER ward?**
_Query_: group by (category, year, ward), summarize (count(total projects))

**Where is this money being spent? Are there blocks that are being repeated?**
* _Query_: group by (block_id, year, ward), summarize (count(total projects) and  summarize (project_cost). 
* We can also make use of the latitude and longitude to conduct simple spatial analysis. Heat map and kernel density analysis are probably the easiest ways to map the “intensity” of spending in a given ward or across the city.  

**Where are the calls coming in from? (Mapping out each 311 call, heat map for each thing)**
* _Query_: PLOT each point, color by category

**Are the projects in the ward addressing the calls proportionally?**
Ratio of 311 calls to menu money projects per category
_Alignment index_
* For each ward/year, calculate % of spending on each category.
* and/or For each ward/year, calculate % of number of projects on each category.
* For each ward/year, calculate % of calls on each category. 
* Calculate difference between these two numbers ^^^ for each category and add them all up. That number is the index for each year/ward.

**Which ward’s projects correspond to its 311 calls most proportionally?**
Sum the above? Or likely an average
_Viz_:
* Plot 311 calls and plot menu money projects? Show a ward with a lot of overlap, show a ward with not a lot of overlap?

