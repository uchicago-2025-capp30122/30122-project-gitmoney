# Final altair 
import csv
import pathlib
import altair as alt
import pandas as pd


# CSV file path
csv_file = pathlib.Path.cwd().parent.parent / "30122-project-gitmoney" / "data" / "calls_money.csv"
print(f"File path: {csv_file}")

def plot_calls_by_year_and_ward(csv_file: pathlib.Path):
    """
    Plot four separate stacked bar charts: calls and money spent by year and ward, categorized.

    Parameters:
        csv_file (Path): Path to CSV file with year, ward, category, calls, and total_cost

    Returns:
        None (displays four plots)
    """
    # Load CSV data directly into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Convert 'year' and 'ward' columns to integer type, 'calls' and 'total_cost' to float
    df['year'] = df['year'].astype(int)
    df['ward'] = df['ward'].astype(int)
    df['calls'] = df['calls'].astype(float)
    df['total_cost'] = df['total_cost'].astype(float)

    # Filter data for years 2019-2023
    df = df[(df['year'] >= 2019) & (df['year'] <= 2023)]

    # Get unique years and wards
    years = sorted(df['year'].unique())
    wards = sorted(df['ward'].unique())

    # Aggregating calls and money by year, ward, and category
    calls_by_year = df.groupby(['year', 'category'])['calls'].sum().unstack()
    money_by_year = df.groupby(['year', 'category'])['total_cost'].sum().unstack()
    calls_by_ward = df.groupby(['ward', 'category'])['calls'].sum().unstack()
    money_by_ward = df.groupby(['ward', 'category'])['total_cost'].sum().unstack()

    # Define the color palette for the categories
    color_palette = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
        '#ffcc00', '#e377c2', '#7f7f7f', '#17becf', '#75701F'
    ]
    categories = df['category'].unique()
    category_colors = {cat: color_palette[i % len(color_palette)] for i, cat in enumerate(categories)}

    # Function to plot the stacked bar chart using Altair
    def plot_stacked_bars(x_values, data, title, x_label, y_label, rotate_x=False):
        melted_data = data.reset_index().melt(id_vars=data.index.name, var_name='category', value_name='value')
        chart = alt.Chart(melted_data).mark_bar().encode(
            x=alt.X(f'{data.index.name}:O', title=x_label, axis=alt.Axis(labelAngle=-90 if rotate_x else 0)),
            y=alt.Y('value:Q', title=y_label, stack='zero'),
            color=alt.Color('category:N', scale=alt.Scale(domain=list(category_colors.keys()), range=list(category_colors.values()))),
            tooltip=[data.index.name, 'category', alt.Tooltip('value:Q', format='.2f')]
        ).properties(
            title=title,
            width=600,
            height=400
        )
        return chart

    # Plot all four charts
    charts = [
        plot_stacked_bars(years, calls_by_year, '311 Calls by Year and Category (2019-2023)', 'Year', 'Number of 311 Calls', rotate_x=False),
        plot_stacked_bars(wards, calls_by_ward, '311 Calls by Ward and Category (2019-2023)', 'Ward', 'Number of 311 Calls', rotate_x=True),
        plot_stacked_bars(years, money_by_year, 'Money Spent by Year and Category (2019-2023)', 'Year', 'Total Money Spent ($)', rotate_x=False),
        plot_stacked_bars(wards, money_by_ward, 'Money Spent by Ward and Category (2019-2023)', 'Ward', 'Total Money Spent ($)', rotate_x=True)
    ]

    # Display all charts
    for chart in charts:
        chart.show()

# Run the real data
if __name__ == "__main__":
    plot_calls_by_year_and_ward(csv_file)
