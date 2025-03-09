# Project Name

Pick a Tag

🚩🛑: WORK IN PROGRESS. See wiki for details 

✅🚴: Good to go. Follow instructions to run

🟡🚧: Done but scripts require lots of hand checking so approach with caution. See instructions

# Goals

# Data Source
How can you get the data?

# Regrets
If you were to re-do the project, would you change anything?

# How to Run

All of subfunctions of gitmoney can be run using the following command:

"uv run gitmoney/run_and_visualize.py".

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
