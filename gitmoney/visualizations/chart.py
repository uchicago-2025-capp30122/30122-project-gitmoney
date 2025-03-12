import csv
import os
from pathlib import Path
import pandas as pd
import altair as alt

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

    # Define output directory 
output_dir = Path.cwd() / "gitmoney/visualizations/charts"
output_dir.mkdir(parents=True, exist_ok=True)


def plot_calls_by_year_and_ward(csv_file: Path) -> None:
    """
    Plot four stacked bar charts: calls and money spent by year and ward, categorized.

    Args:
        csv_file (Path): Path to CSV file with year, ward, category, calls, and total_cost

    Returns:
        None (saves four HTML files in the visualizations directory)
    """

    # Load and preprocess data
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
    
    return aggregations

def create_chart(data: pd.DataFrame, title: str, x_label: str, y_label: str, rotate_x: bool = False) -> alt.Chart:
        """
        Create an Altair bar chart.

        Args:
            data (pd.DataFrame): Aggregated data for the chart.
            title (str): Chart title.
            x_label (str): Label for the x-axis.
            y_label (str): Label for the y-axis.
            rotate_x (bool): Whether to rotate x-axis labels.

        Returns:
            alt.Chart: Altair chart object.
        """
        melted_data = data.reset_index().melt(
            id_vars=data.index.name,
            var_name='category',
            value_name='value'
        )

        chart = (alt.Chart(melted_data)
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
                     #title=title,
                     width=CHART_WIDTH,
                     height=CHART_HEIGHT
                 )
                 .configure_axis(
                     labelFontSize=15,
                     titleFontSize=20,
                     grid=False
                 )
                 .configure_title(
                     fontSize=30
                 )
                 .configure_legend(
                     labelFontSize=18,
                     titleFontSize=20,
                     orient='right',
                     labelLimit=500
                 )
                 .interactive())

        return chart
    
def combined():
    """
    Aggregate data and create charts
    """
    aggregations = plot_calls_by_year_and_ward('gitmoney/data/clean_csvs/calls_money.csv')

    # Define chart configurations with filenames based on titles
    chart_configs = [
        ('calls_by_year', '311 Calls by Year and Category (2019-2023)', 'Year', 'Number of 311 Calls', False),
        ('calls_by_ward', '311 Calls by Ward and Category (2019-2023)', 'Ward', 'Number of 311 Calls', True),
        ('money_by_year', 'Money Spent by Year and Category (2019-2023)', 'Year', 'Total Money Spent ($)', False),
        ('money_by_ward', 'Money Spent by Ward and Category (2019-2023)', 'Ward', 'Total Money Spent ($)', True)
    ]

    # Generate and save charts as HTML files with titles as filenames
    for key, title, x_label, y_label, rotate in chart_configs:
        # Convert title to a valid filename: replace spaces with underscores, remove parentheses
        filename = title.replace(' ', '_').replace('(', '').replace(')', '') + '.html'
        filepath = output_dir / filename
        chart = create_chart(aggregations[key], title, x_label, y_label, rotate)
        chart.save(str(filepath))
        print(f"Saved {filepath}")

if __name__ == "__main__":
    # Define the CSV file path relative to the visualizations directory
    cwd = Path(os.getcwd())
    csv_file = cwd.parent.parent / "gitmoney" / "data" / "calls_money.csv"
    print(f"File path: {csv_file}")
    plot_calls_by_year_and_ward(csv_file)