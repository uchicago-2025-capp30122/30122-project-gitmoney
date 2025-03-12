import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import csv
from gitmoney.visualizations.colors import year_colors_df
import sys
import os
from pathlib import Path

data_file = Path(__file__).parent.parent / "data/"
chart_file = Path(__file__).parent.parent / "visualizations/charts"

def num_proj_chart_build():
    # Read in and clean data
    calls_money = pd.read_csv(data_file/"calls_money.csv")

    # Create good dataframe with sorted years and colors
    calls_money_19_23 = calls_money.query('year >= 2019 and year <= 2023')

    calls_money_19_23= calls_money_19_23.sort_values(by='year', ascending=False)

    calls_money_19_23['year'] = calls_money_19_23['year'].astype(str)

    calls_money_19_23 = calls_money_19_23.merge(year_colors_df, on=["year"])
    
    # Group data by year, total projects
    
    num_projects_ward_year = pd.DataFrame(calls_money_19_23.\
        groupby(['ward', 'year', 'color']).size().\
            rename('Number Projects in Year').reset_index())
    num_projects_ward_total = pd.DataFrame(calls_money_19_23.\
        groupby(['ward']).size().rename('Total Projects, 2019-23').\
            reset_index())
        
    num_projects_ward = num_projects_ward_year.\
        merge(num_projects_ward_total, on=["ward"]).\
            rename(columns={"ward": "Ward", "year": "Year"})

    # Create Chart
    
    chart = alt.Chart(num_projects_ward).mark_bar().encode(
        x='Ward',
        y='Total Projects, 2019-23',
        color=alt.Color('Year', \
            scale=alt.Scale(domain=num_projects_ward['Year'].tolist(), \
                range=num_projects_ward['color'].tolist())),
        order=alt.Order(
        'Year',
        sort='ascending'),
        tooltip=['Ward', 'Year', 'Number Projects in Year', 'Total Projects, 2019-23'],
    ).properties(
            width=750,
            height=450,
        ).interactive()
    
    chart.save(chart_file/'num_projects_per_ward.html')
