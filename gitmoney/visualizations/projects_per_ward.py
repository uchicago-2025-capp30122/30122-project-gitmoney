from colors import cat_colors_df
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import csv

def num_proj_chart_build():
    # Read in and clean data
    calls_money = pd.read_csv("../data/calls_money.csv")

    calls_money["year"] = pd.to_numeric(calls_money["year"])

    calls_money_18_23 = calls_money.query('year >= 2019 and year <= 2023')

    calls_money_18_23 = calls_money_18_23.merge(cat_colors_df, on="category").rename(columns={"ward": "Ward"})
    
    # Create good dataframe
    
    num_projects_ward = pd.DataFrame(calls_money_18_23.groupby(['Ward']).size().rename('Number Projects, 2019-23').reset_index())
    
    chart = alt.Chart(num_projects_ward).mark_bar().encode(
    x='Ward',
    y='Number Projects, 2019-23',
    #color=alt.Color('color').scale(None),
    tooltip=['Ward', 'Number Projects, 2019-23'],
).interactive()
    
    chart.save('charts/num_projects_per_ward.html')
