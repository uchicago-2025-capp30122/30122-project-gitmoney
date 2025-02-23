**WHO** — Alderpeople, Chicago Citizens <br>
**WHAT** — 311 Calls (see categories), Menu Money Projects (see categories) <br>
**WHEN** — year (2012-2023) <br>
**WHERE** — (Lat, long) for 311 coords, project coordinates; ward shape <br>
**WHY** — government accountability, highlight need versus solutions enacted <br>
<br>
# GOALS
Visualizing problem areas, where people have concerns

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

