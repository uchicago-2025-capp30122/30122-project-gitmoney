# Git Money Milestone 2
## Abstract

Our core idea is to make a data visualization that combines public Chicago data — **specifically 311 data** — with web-scraped data tabulating aldermanic expenditures through the "menu" program by district. GIS ward boundaries are available and can be easily incorporated. We will scrape wikipedia to gain additional data about alders and their time in office. Chicago Data Portal offers an API endpoint for us to extract data from, so we can utilize this for any of the three datasets from that source.

![MV5BNzIxZmIzYjEtZGMyZi00NDAwLWJmODktYTAwOWU2ZjkwZjdlXkEyXkFqcGc@ _V1_FMjpg_UX1000_](https://github.com/user-attachments/assets/39e69571-015b-464d-b5f2-68171f03dff6)

<img width="1015" alt="406695689-2a4a6727-acf6-4c5d-9dcf-df3a5dbad6d4" src="https://github.com/user-attachments/assets/37a28769-0eef-4d97-9d32-1490de54dc33" />

## Data Sources
### Data Reconciliation Plan

An important thing to do at this step is to have a plan for how data from your various sources will be brought together.

For each data set, you will need to identify the "unique key" that will allow you to connect it to other data sets. (We'll discuss this in more detail.)

Both 311 and menumoney datasets have issue categories (“sr_type” for 311 calls/complaints and “category” for menu money spending). For both we’ll have to create unique buckets for an overall category variable. 

We’ll also match on year and ward (or potentially street segment). Ward/year data will also allow us to pull in the respective alderperson via the wikipedia scraping data.

Then for each year/ward, we’ll be able to see what the biggest proportion of 311 calls are and what the biggest proportion of menu money spending is and how they correlate.
### Data Source #1: JakeJSmith's scraped Alder menu money database
The Aldermanic menu money database does not have a unique identifier. We will assign it a row-number index that can be used to identify each row, but this data must be joined spatially. Luckily, we can aggregate at the Aldermanic ward level, for starters. This will allow us to compare the data with 311 calls, which have latitude and longitude in addition to an already available ward number field. 

In total, this dataset has 28,108 rows of data spanning over a decade of menu spending. It has six fields (columns) to analyze. So far, we have successfully created a function to extract a list of named addresses, and a corresponding Streets dictionary that can be used to search cross streets.

You can find exploration of this dataset in our data_smells folder. Our primary concerns are two negative entries, duplicate rows, and entries with two years in the description (which is not seen in our exploration). These do correspond to the PDFs, and they are not data entry errors from Jake. We have been in communication with one of the wards to gain insight into how data is collected (upon Jake Smith’s recommendation), but we may need to attempt to reach out to specific wards to learn about specific mistakes (such as negative money). 

**Data URL**:  https://docs.google.com/spreadsheets/d/1MZpUnD8bXceRw-P3fiTZtH7KtSunNaEYa-xpapWw1Ho/edit

**Additional URLs**:
https://github.com/jakejsmith/ChicagoMenuMoney/blob/main/data-dictionary.md

**Data Access**: Bulk Data

**Unique Key(s)**: 
_Year_ - joining to 311
_Category_ - joining to 311 (pending 311 data cleaning)
_Description/Ward_ - joining to 311's lat/long columns with help from Alex's [geomoney scripts](https://github.com/uchicago-2025-capp30122/30122-project-gitmoney/tree/main/geomoney). If that goes south, we join on ward

**Rows and Columns**: 
28k rows and 6 columns

**Challenges**: 
_Geo-cleaning_
The menu money data contains locational information as a string in the “Description” column. In some cases, there is a geocodable address, in other cases, there are street names along with a cross street name or two. For all these cases, we are using a multi-step cleaning process:
Create a dictionary in which a street name indexes all rows that share that street name. For each of these street segments, there are TO_CROSS and FROM_CROSS street segments listed by segment ID. 
Search the set of known street names for matches in the “Description” field, to create a list of street names reported by the project. Most Descriptions follow one of two formats: ON_STREET/ FROM_CROSS, TO_CROSS or ON_STREET/FROM_CROSS
Using this dictionary, we can search for the intersections listed in the menu money dataset to identify specific street segments for menu projects. 

Once the menu data is at the street segment level, we will be able to join 311s (using latitude/longitude) at the street level. 

**Miscellaneous info about this dataset**

_Advice from Jake_
We are working with Jake Smith (dataset creator) to better understand the Menu Money. He pushed us to understand how menu money projects, (which isn't a terrible idea so we looked into that). 

```
Response from 49th ward:

How do Alderpeople decide what to spend menu money on?

PB usually starts with “discretionary funds”—money that is not set aside for fixed or essential expenses and that is instead allocated at the discretion of officials or staff. While this is typically a small part of the overall budget, it is a big part of the funds that are available and up for debate each year. There are many sources of discretionary money. It could come from the capital budget (for physical infrastructure) or the operating budget (for programs and services) of your city, county, or state. City councilors or other officials could set aside their individual discretionary funds, as has been done in Chicago.

Elected officials may also have control over special allocations like Community Development Block Grants or Tax Increment Financing (TIF) money.The funds could even come from non-governmental sources like foundations, community organizations, or grassroots fundraising, if this money is oriented towards public or community projects. Some PB processes mix funds from different sources, to build up a bigger budget pot.

Do 311 calls from constituents about infrastructure problems play a role in this decision making?

311 Calls regarding infrastructure plays a part in idea collection for the PB cycle based upon the type of 311 case. We try to have CDOT address 311 issues promptly to avoid major street damages or issues, however, if there are project based solutions that can be PB allocated for a longer term solution, we can add it as a project for the community to vote on.

How else do constituents make their priorities known?

While every PB process is different, most follow a similar structure: a SteeringCommittee (SC) made of community volunteers develops the rules that will guide the process, residents brainstorm spending ideas, volunteer budget delegates develop proposals based on these ideas, residents vote on proposals, and the top projects are implemented."
```
### Data Source 2: Chicago Data Portal/API: Contract Data

Intro <br>
It feels expansive — both in number of rows/columns and in the number of categories in that we’ll have to bucket in the sr_type. However, it’s also well documented and pretty straightforward to access.

**Data URL**:  https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/about_data

**Data Access**: API

**Challenges**: 
Connecting: The service requests will need to be spatially linked to the GIS ward boundaries listed below.
Categorizing/connecting: We need to categorize the 50+ 311 call categories to match the menu money categories
Storage: The data has millions of rows, so need to figure out where/how to keep it
Missing data: Wards and location data is occasionally empty
Duplicate handling: Serial numbers are unique, but some requests are children of a previous request. And those children do not look like their parents in concerning ways. For instance, request: “SR19-00001060” is the child of “SR19-01048953.” They have the same address, but different wards listed. So that’s not fun. There is a duplicate column in the data, and we could filter data to only keep the parent request. But we may need to map lat long coordinates inside wards ourselves to be 100% of data accuracy. This problem also relates to 2.2’s challenge of looking at how/if ward boundaries changed. 

**Rows and columns**
<br>
The dataset has 11 million rows and 50 columns, but with filtering we should be able to reduce the rows and we’ll get the columns down to about 14 ones we actually want. <br>
<br>
Columns <br>
sr_number <br>
sr_type <br>
status <br>
created_date <br>
last_modified_date <br>
closed_date <br>
street_address <br>
street_number <br>
street_direction <br>
street_name <br>
Duplicate <br>
parent <br>
legacy_sr_number <br>
ward <br>
location <br>
<br>
### Data Source #3: Wikipedia list of Chicago alders by year since 1923

- Is the data coming from a webpage, bulk data, or an API?
The data is coming from a webpage. 

- Are there any challenges or remaining uncertainty about the data?
No challenge. 

- How many records (rows) does your data set have?
The data has 159 rows and 4 columns. 

- How many properties (columns) does your data set have?
The data set has 4 columns: Alderperon, Term in office, Party and Notes. 

- Write a few sentences about your exploration of the data set. At this point you should have 
downloaded some of the data and explored it with an eye for things that might cause issues for your project
The dataset has a list of Chicago alderpersons by ward since 1923. 

For each source please identify:
**Data URL**:  
https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923
**Data Access**: Web Scraping

**Challenges**: 

This data will need to be scraped and stored, but it will provide us with names and terms lengths for different alders, allowing for another dimension of analysis

We’ve scraped tables and text, thus far. The text portion of wikipedia will require us to scrape links on the original wikipedia page.  
## Project Plan
We have split into teams to collect data. 

**Getnet & Libby**: Wikipedia
**Riley**: 311
**Alex**: Menu Money: Description Geocoding

#### Week 5
Each of us has started the process to create a nice dataset. We will meet again later this week to check back on our progress, but we are feeling confident in our abilities to build each dataset.

#### Week 6
Our next phase will be joining the data together. We will need to devote a lot of effort into 311 data cleaning and categorizing data to match with menu money. We have started that process by narrowing down eliminating (311 complaints)[https://docs.google.com/spreadsheets/d/1rSP1FfalIyaVh1LS06mz4KoEDyrgHWrzMs4479JBpmA/edit?usp=sharing]. But we will need to put these categories into Menu Money spending categories. Riley and Libby may end up doing this. 

We also will need to join our geodata to Menu Money data. Alex is in charge of this aspect. Aldermen will need to be joined to the Menu Money dataset, and Getnet will likely be in charge of this. Ideally, all joining would be finished by Week 6. 

#### Week 7
We’ll begin analyzing and building data in Week 7. If all goes smoothly, we should be able to map the majority of 311 calls and the majority of menu money projects and find overlap. From there, we can learn more about the project’s interface.
## Questions

1) Can our command line interface just produce a GUI? Or are you asking us to produce a map into the command line? (Please say GUI)
2) How do we store data for this project? 311 data is going to have MILLIONS of rows, and github will be sad and overwhelmed. Do you recommend Box? OneDrive? 
3) What are your thoughts on how to present/visualize this data? What package(s)?  What do you consider when you’re preparing a visualization?



