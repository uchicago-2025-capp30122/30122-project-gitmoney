# Final Version
import csv
import pathlib
from typing import List
import altair as alt
import pandas as pd

def plot_calls_by_year_and_ward(csv_file: pathlib.Path) -> None:
    """
    Plot four stacked bar charts: calls and money spent by year and ward, categorized.

    Args:
        csv_file (pathlib.Path): Path to CSV file with year, ward, category, calls, and total_cost

    Returns:
        None (displays four plots)
    """
    # Define constants
    YEAR_RANGE = range(2019, 2024)  
    CAT_COLORS = {
        "Beautification": "#8B648B",
        "Bike Infrastructure": "#F8C8F1",
        "Lighting": "#E89545",
        "Parks & Recreation": "#5DB7B7",
        "Plants, Gardens, & Sustainability": "#82B65B",
        "Schools & Libraries": "#cdcb44",
        "Security Cameras": "#294896",
        "Streets & Transportation": "#BE5151"
    }
    CHART_WIDTH = 600
    CHART_HEIGHT = 400

    # Load and preprocess data once
    df = (pd.read_csv(csv_file)
          .assign(
              year=lambda x: x['year'].astype(int),
              ward=lambda x: x['ward'].astype(int),
              calls=lambda x: x['calls'].astype(float),
              total_cost=lambda x: x['total_cost'].astype(float)
          )
          .query('year in @YEAR_RANGE')
          .groupby(['year', 'ward', 'category'])[['calls', 'total_cost']]
          .sum()
          .reset_index())

    # Prepare aggregated data
    aggregations = {
        'calls_by_year': df.groupby(['year', 'category'])['calls'].sum().unstack(),
        'money_by_year': df.groupby(['year', 'category'])['total_cost'].sum().unstack(),
        'calls_by_ward': df.groupby(['ward', 'category'])['calls'].sum().unstack(),
        'money_by_ward': df.groupby(['ward', 'category'])['total_cost'].sum().unstack()
    }

    def create_chart(data: pd.DataFrame, title: str, x_label: str, y_label: str, rotate_x: bool = False) -> alt.Chart:
       
        melted_data = data.reset_index().melt(
            id_vars=data.index.name,
            var_name='category',
            value_name='value'
        )
        
        return (alt.Chart(melted_data)
                .mark_bar()
                .encode(
                    x=alt.X(f'{data.index.name}:O', 
                           title=x_label,
                           axis=alt.Axis(labelAngle=-90 if rotate_x else 0)),
                    y=alt.Y('value:Q', title=y_label, stack='zero'),
                    color=alt.Color('category:N',
                                  scale=alt.Scale(domain=list(CAT_COLORS.keys()),
                                                range=list(CAT_COLORS.values()))),
                    tooltip=[data.index.name, 'category', alt.Tooltip('value:Q', format='.2f')]
                )
                .properties(
                    title=title,
                    width=CHART_WIDTH,
                    height=CHART_HEIGHT
                ))

    # Define chart configurations
    chart_configs = [
        ('calls_by_year', '311 Calls by Year and Category (2019-2023)', 'Year', 'Number of 311 Calls', False),
        ('calls_by_ward', '311 Calls by Ward and Category (2019-2023)', 'Ward', 'Number of 311 Calls', True),
        ('money_by_year', 'Money Spent by Year and Category (2019-2023)', 'Year', 'Total Money Spent ($)', False),
        ('money_by_ward', 'Money Spent by Ward and Category (2019-2023)', 'Ward', 'Total Money Spent ($)', True)
    ]

    # Generate and display charts
    charts = [create_chart(aggregations[key], title, x_label, y_label, rotate)
             for key, title, x_label, y_label, rotate in chart_configs]
    
    # Altair's concatenation (Remove later)
    '''
    try:
        alt.vconcat(*charts).show()
    except AttributeError:'''
    for chart in charts:
        chart.show()

if __name__ == "__main__":
    csv_file = pathlib.Path.cwd().parent.parent / "30122-project-gitmoney" / "data" / "calls_money.csv"
    print(f"File path: {csv_file}")
    plot_calls_by_year_and_ward(csv_file)