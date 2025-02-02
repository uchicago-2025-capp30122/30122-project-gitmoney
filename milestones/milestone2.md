# Git Money Milestone 2

## Abstract

This is the same: 

Our core idea is to make a data visualization that combines public Chicago data — **specifically 311 data** — with web-scraped data tabulating aldermanic expenditures through the "menu" program by district. GIS ward boundaries are available and can be easily incorporated. We will scrape wikipedia to gain additional data about alders and their time in office. Chicago Data Portal offers an API endpoint for us to extract data from, so we can utilize this for any of the three datasets from that source.

![MV5BNzIxZmIzYjEtZGMyZi00NDAwLWJmODktYTAwOWU2ZjkwZjdlXkEyXkFqcGc@ _V1_FMjpg_UX1000_](https://github.com/user-attachments/assets/39e69571-015b-464d-b5f2-68171f03dff6)

<img width="1015" alt="406695689-2a4a6727-acf6-4c5d-9dcf-df3a5dbad6d4" src="https://github.com/user-attachments/assets/37a28769-0eef-4d97-9d32-1490de54dc33" />

## Data Sources

### Data Reconciliation Plan

An important thing to do at this step is to have a plan for how data from your various sources will be brought together.

For each data set, you will need to identify the "unique key" that will allow you to connect it to other data sets. (We'll discuss this in more detail.)

Additionally, for each data source, add a section like:

### Data Source #1: JakeJSmith's scraped Alder menu money database

**Data URL**:  https://docs.google.com/spreadsheets/d/1MZpUnD8bXceRw-P3fiTZtH7KtSunNaEYa-xpapWw1Ho/edit

**Additional URLs**:
https://github.com/jakejsmith/ChicagoMenuMoney/blob/main/data-dictionary.md

**Data Access**: Bulk Data

**Unique Key(s)**: 
_Year_ - joining to 311
_Category_ - joining to 311 (pending 311 data cleaning)
_Description/Ward_ - joining to 311's lat/long columns with help from Alex's [geomoney scripts](https://github.com/uchicago-2025-capp30122/30122-project-gitmoney/tree/main/geomoney). If that goes south, we join on ward

**Challenges**: 
_Geo-cleaning_
insert Alex



_Advice from Jake_
We are working with Jake Smith (dataset creator) to better understand the Menu Money. He pushed us to understand how menu money projects, (which isn't a terrible idea so we looked into that). 

```
Response from 49th ward:

How do Alderpeople decide what to spend menu money on?

PB usually starts with “discretionary funds”—money that is not set aside for
fixed or essential expenses and that is instead allocated at the discretion of
officials or staff. While this is typically a small part of the overall budget, it is a
big part of the funds that are available and up for debate each year.
There are many sources of discretionary money. It could come from the capital
budget (for physical infrastructure) or the operating budget (for programs and
services) of your city, county, or state. City councilors or other officials could
set aside their individual discretionary funds, as has been done in Chicago.
Elected officials may also have control over special allocations like
Community Development Block Grants or Tax Increment Financing (TIF)
money.The funds could even come from non-governmental sources like foundations, community
organizations, or grassroots fundraising, if this money is oriented towards public or community projects.
Some PB processes mix funds from different sources, to build up a bigger budget pot.

Do 311 calls from constituents about infrastructure problems play a role in this decision making?

311 Calls regarding infrastructure plays a part in idea collection for the PB cycle
based upon the type of 311 case. We try to have CDOT address 311 issues promptly to avoid
major street damages or issues, however, if there are project based solutions that can be
PB allocated for a longer term solution, we can add it as a project for the community to vote on.

How else do constituents make their priorities known?

While every PB process is different, most follow a similar structure: a SteeringCommittee
(SC) made of community volunteers develops the rules that will guide the process, residents brainstorm
spending ideas, volunteer budget delegates develop proposals based on these ideas, residents vote on proposals,
and the top projects are implemented."
```




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



- Is the data coming from a webpage, bulk data, or an API?
- Are there any challenges or remaining uncertainity about the data?
- How many records (rows) does your data set have?
- How many properties (columns) does your data set have?
- Write a few sentences about your exploration of the data set. At this point you should have downloaded some of the data and explored it with an eye for things that might cause issues for your project.

## Project Plan

Please provide a project plan that will help keep your team on track.

It is recommended that you:

- Identify required (and optional) components of the project to be built.
- Have a plan that makes it clear what will be built by Milestone #3 (it may be helpful to break this out weekly for the remainder of the quarter) and what will be built by the final project.
- For each component, identify who is primarily responsible, and who else might work on it with them.

## Questions

1) Can our command line interface just produce a GUI? Or are you asking us to produce a map into the command line? (Please say GUI)
2) How do we store data for this project? 311 data is going to have MILLIONS of rows, and github will be sad and overwhelmed. Do you recommend Box? OneDrive? 
