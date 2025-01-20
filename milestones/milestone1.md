# GitMoney
## Members

- Libby Seline <eseline@uchicago.edu>
- Riley Morrison <rileymo@uchicago.edu>
- Alex McMurtry <amcmurtry@uchicago.edu>
- Getnet Dejene <getnet@uchicago.edu>
## Abstract

Our core idea is to make a data visualization that combines public Chicago data with web-scraped data tabulating aldermanic expenditures through the "menu" program by district. GIS ward boundaries are available and can be easily incorporated. We will scrape wikipedia to gain additional data about alders and their time in office. Chicago Data Portal offers an API endpoint for us to extract data from, so we can utilize this for any of the three datasets from that source.
## Preliminary Data Sources
### Data Source #1: JakeJSmith's scraped Alder menu money database

**Data URL**:  https://docs.google.com/spreadsheets/d/1MZpUnD8bXceRw-P3fiTZtH7KtSunNaEYa-xpapWw1Ho/edit

These are collected from quarterly menu money reports compiled by the alders.

**Additional URLs**:
https://github.com/jakejsmith/ChicagoMenuMoney/blob/main/data-dictionary.md

**Data Access**: Bulk Data

**Challenges**: 
Duplicates & lack of identifying columns

There are no identifying columns and that led to the discovery of duplicates in the dataset. Albeit — very few. All but one of them is associated with the “‘In-Road’ State Law Stop for Pedestrians Signs,” so there must be some sort of pattern there that we may need to ask about. We do have access to the PDFs used to create this data, so we can look back and see where the discontinuity could come from. Additionally, the guy who created this database is a Harris alum so we imagine he would be pretty useful when debugging. Though it has been a year since he published this so hopefully he can point out why this occurred. 

Below is the dataset of duplicates where “n” is the number of times the dataset appears. 
<img width="825" alt="Screenshot 2025-01-19 at 8 32 37 PM" src="https://github.com/user-attachments/assets/32913634-23a3-4b9f-b8a6-4323aef1bfc5" />

Good news is that the categories are consistent and the GitHub explains how categorization worked. 

Description & program columns are messy and thus obsolete — and raise questions about rest of columns (described by Libby)

The good news is that most of the data is complete, and I think we don’t need the information missing to complete our project goal. 

There are 3 missing program variables, and each has the category miscellaneous. There is a description with each of the three missing variables. There are missing descriptions for 109 rows, but each of these has a program. See the missing data here.

Looking at this has made me realize that the program and description data are highly specific and inconsistent, and we generally can’t see all of the spending for a specific project. That’s not the point of our analysis. Though I have highlighted a few rows that make me question the validity of different entries. For instance, in just this sample of 100 rows, there are instances in which a row could be for two years. Though I think the project is listed twice. So, I generally wonder if there are mistakes hidden in entries like this. 
### Data Source 2
#### 2.1: Chicago Data Portal/API: Contract Data

**Data URL**:  https://data.cityofchicago.org/Service-Requests/311-Service-Requests/v6vf-nfxy/about_data

**Data Access**: API

**Challenges**: 
The service requests will need to be spatially linked to the GIS ward boundaries listed below.

Wards and location data is occasionally empty

We downloaded a sample of 311 data that shows the first two weeks worth of 311 requests in 2019. This sample showed that 2% of data doesn’t have a ward listed. That’s not great, but most of this data does have a street address (169/176) listed so if we really want to, we can geocode these. But I think we can get away with omitting 2% of the data. 

Serial numbers are unique, but some requests are children of a previous request. And those children do not look like their parents in concerning ways. 

For instance, request: “SR19-00001060” is the child of “SR19-01048953.” They have the same address, but different wards listed. So that’s not fun. There is a duplicate column in the data, and we could filter data to only keep the parent request. But we may need to map lat long coordinates inside wards ourselves to be 100% of data accuracy. This problem also relates to 2.2’s challenge of looking at how/if ward boundaries changed. 
#### 2.2: Chicago Data Portal/API: GIS ward boundaries
**Data URL**:  
https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Ward-Offices/htai-wnw4/about_data
**Data Access**: API

**Challenges**: 
Chicago's aldermanic wards with geographic boundaries. It will be important to validate when these boundaries were last changed to assess how significantly changes could affect our analysis.
#### 2.3: Chicago Data Portal/API: Contract Data
**Data URL**:  
https://data.cityofchicago.org/Administration-Finance/Contracts/rsxa-ify5/about_data
**Data Access**: API
**Challenges**: 
Geocoding
The data doesn’t have geocoded addresses, but it does have addresses listed for most of the data. So, we should be able to match up a contract with a specific ward and an alderman. We do have geocoding experience on the team, so we feel confident we can overcome this obstacle. 

We also have put on our tin foil hats because we know there is previous corruption between menu money and aldermen. 
### Data Source #3: 
#### 3.1: Wikipedia list of Chicago alders by year since 1923

For each source please identify:
**Data URL**:  
https://en.wikipedia.org/wiki/List_of_Chicago_alderpersons_since_1923
**Data Access**: Web Scraping
**Challenges**: 

This data will need to be scraped and stored, but it will provide us with names and terms lengths for different alders, allowing for another dimension of analysis

.#### 3.2: BACKUP: Chicago Election Results
**Data URL**:
https://chicagoelections.gov/elections/results
**Data Access**: Web Scraping
**Challenges**: 
In case you hate the idea of us scraping Wikipedia, we could alternatively scrape data from here. 

This method is harder, but we have a more official source. We will need to use a package like selenium to be able to custom search for each election, grab the election results, and put the data into a file. Though, I wonder if this data will cover cases where an alderman is not elected but appointed due to unforeseen circumstances …

.#### 3.3: BACKUP: Chicago Councilmatic
**Data URL**:
https://chicago.councilmatic.org/compare-council-members/ OR
https://chicago.councilmatic.org/search/

**Data Access**: Web Scraping
**Challenges**: 
In case you hate the idea of us scraping Wikipedia, we could alternatively scrape data from here. 

This website doesn’t currently host all of the past aldermen. We would have to figure out aldermen by scraping from the legislation portion, which lists aldermen and their ward with introduced legislation. So, we could work with that. 

They do have a Github repository that manages their website publication, so I wonder if we could just look at past commits to the people page. But we’d have to dive into their repo to understand just where this information is stored. And it looks like they’ve reorganized quite a bit so searching past legislation may be our best bet — and a pain in the butt. 
## Preliminary Project Plan
Our primary goal is a data visualization that combines GIS ward boundaries, aldermanic menu money expenditures by ward, and 311 calls to tabulate and visualize the expenditures. We will scrape Wikipedia to form a database with the alder's name and term length. It offers another degree of variation.

We also hope to include contract data by geocoding addresses seen in contract data. 
## Questions
A **numbered** list of questions for us to respond to.
1. What is the link between aldermanic spending and 311 calls? <br>
  a. Do the categories of aldermanic spending projects align with concerns addressed in 311 calls? <br>
  b. How does that change over time? <br>
    i. If an alderman pours money into a problem, do 311 calls related to that category decrease the next year? 
2. Are there conspicuous patterns of aldermen using a common contractor? <br>
  a. How much money is a contractor receiving per ward? <br>
  b. What types of projects are contractors working on?













## Backup Project
NYC Congestion Toll Impact Analysis/Visualization
## Abstract
New York City's congestion pricing law has officially taken effect, charging vehicles that enter Manhattan below 60th Street. This initiative aims to reduce traffic congestion, improve air quality, and generate funds to support public transportation improvements. The goal of this project is to analyze traffic, subway/bus ridership, and car crash data to evaluate the impact of the congestion pricing law on the city's transportation system. Specifically, we aim to determine whether the congestion pricing policy has contributed to the key objectives outlined by the state government—reducing congestion and promoting sustainable transportation options.
## Preliminary Data Sources
### Data Source #1: Data City of New York
- https://data.cityofnewyork.us/Transportation/DOT-Traffic-Speeds-NBE/i4gi-tjb9/data
- Data coming from a webpage
- Are there any challenges or uncertainty about the data at this point?
### Data Source #2: NY Citywide Traffic Statistics
- https://www.nyc.gov/site/nypd/stats/traffic-data/traffic-data-trafficstat.page
- Data coming from a webpage
- Are there any challenges or uncertainty about the data at this point?
### Data Source #3: Google Maps traffic data
- A URL to the data source.
- Data coming from API
- Are there any challenges or uncertainty about the data at this point?
## Preliminary Project Plan
Our primary goal is to evaluate the effectiveness of New York City's congestion pricing law in reducing traffic, increasing public transit ridership, and improving road safety. The aim is to analyze traffic, ridership, and crash data before and after the policy's implementation and provide data visualizations to illustrate its impact.
 
