#### Data Visualization

import pandas as pd
import pathlib
import shapely.wkt
import geopandas as gpd
import pydeck as pdk
import numpy as np
import random

def cost_to_color(cost_value, min_cost, max_cost):
    """
    Map cost value to a color on a gradient scale
    
    Args:
    cost_value (float): The cost value to map to a color.
    min_cost (float): The minimum cost value in the dataset.
    max_cost (float): The maximum cost value in the dataset.

    Returns:
    list: A list of RGBA values representing the color.
    """
    cost_range = max_cost - min_cost
    if cost_range == 0:  # Avoid division by zero
        normalized = 0
    else:
        normalized = (cost_value - min_cost) / cost_range
    
    # Create a color gradient from blue (low cost) to red (high cost)
    r = int(255 * normalized)
    g = int(0)
    b = int(255 * (1 - normalized))
    
    return [r, g, b, 255]  # RGBA


def convert_cost(cost):
    """
    Convert a cost string to a float, removing currency symbols and commas
    
    Args:
    cost (str or float): The cost value to convert.

    Returns:
    float: The cost value as a float.

    """
    try:
        # First remove any currency symbols and commas
        if isinstance(cost, str):
            cost_str = cost.replace('$', '').replace(',', '')
            cost_float = float(cost_str)
        else:
            cost_float = float(cost)
    except (ValueError, TypeError):
        # If conversion fails, set to 0
        cost_float = 0.0
    return cost_float

def create_data_df():
    """
    Load the data and perform a spatial join between the menu money and streets data

    Returns:
    GeoDataFrame: A GeoDataFrame containing the joined data.
    """

    # load the data
    mm_csv = pathlib.Path.cwd() / 'gitmoney/data/final_menu_money.csv' 
    streets_csv = pathlib.Path.cwd() / 'gitmoney/data/streets.csv' 
    mm_df = pd.read_csv(mm_csv).drop_duplicates()
    streets_df = pd.read_csv(streets_csv)
    aldermanic_fp = pathlib.Path.cwd() / 'gitmoney/data/calls_money_pivot_with_alder.csv'
    aldermanic_data = pd.read_csv(aldermanic_fp)
    
    # convert the 'the_geom' column from WKT strings to geometry objects
    streets_df['geometry'] = streets_df['the_geom'].apply(shapely.wkt.loads)
    
    # create a GeoDataFrame
    streets_gdf = gpd.GeoDataFrame(streets_df, geometry='geometry')
    streets_gdf.crs = 'EPSG:4326'

    # perform the join operation
    geo_mm_df = streets_gdf.merge(mm_df,
                                  left_on='OBJECTID',
                                  right_on='OBJECTID',
                                  how='inner',
                                  suffixes=('_st', '_mm'))
    geo_mm_df = geo_mm_df.merge(aldermanic_data,
                                left_on=['ward', 'year', 'category'],
                                right_on=['Clean Ward', 'year', 'category'],
                                how='left')
    geo_mm_df = geo_mm_df.drop_duplicates()
    geo_mm_df = geo_mm_df[geo_mm_df['year'].isin([2019, 2020, 2021, 2022, 2023])]
    
    # crs to (EPSG:4326) for web maps
    geo_mm_df = geo_mm_df.to_crs(epsg=4326)
    geo_mm_df['cost'] = geo_mm_df['cost'].apply(convert_cost)
    return geo_mm_df

def create_visualization(geo_mm_df):
    """
    Create a Pydeck visualization of the extracted menu money streets on a map

    Args:
    geo_mm_df (GeoDataFrame): The GeoDataFrame containing the menu money-streets data.

    No return value, but saves the visualization to an HTML file.
    """

    # calculate mean latitude and longitude for the viewport
    mean_lat = geo_mm_df.geometry.centroid.y.mean()
    mean_lon = geo_mm_df.geometry.centroid.x.mean()

    # prepare data for Pydeck
    path_data = []
    zipped = zip(
        geo_mm_df.geometry,
        geo_mm_df.year,
        geo_mm_df.cost,
        geo_mm_df.category,
        geo_mm_df.description,
        geo_mm_df.ward,
        geo_mm_df.Alderperson,
        geo_mm_df.calls,
        geo_mm_df.num_projects,
        )
    for feature, year, cost, category, description, ward, alder, calls, num_projects in zipped:
        
        # convert WKT string to geometry object if necessary
        if isinstance(feature, str):
            feature = shapely.wkt.loads(feature)
        
        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        
        # change this section to use lists instead of tuples for coordinates
        for linestring in linestrings:
            # get coordinates as LISTS instead of tuples, ensure they're in [longitude, latitude] format
            coords = [[float(lon), float(lat)] for lon, lat in zip(linestring.xy[0], linestring.xy[1])]
            if len(coords) >= 2:  # Only add if we have at least 2 coordinates (a valid line)
                path_data.append({
                    'path': coords,
                    'name': f"{alder} - {description}",
                    'year': str(year),
                    'cost': str(cost),
                    'category': str(category),
                    'description': str(description),
                    'ward': str(ward),
                    'alderman': str(alder),
                    'calls': str(calls),
                    'num_projects': str(num_projects)
                })


    # add color to each path based on category
    for path in path_data:
        # cost to color
        cost = float(path['cost'])
        min_cost = geo_mm_df['cost'].min()
        max_cost = geo_mm_df['cost'].max()
        color = cost_to_color(cost, min_cost, max_cost)
        path['color'] = color

    # update layer to use the color field
    layer = pdk.Layer(
        'PathLayer',
        data=path_data,
        get_path='path',
        get_color='color'
        get_width=10, 
        pickable=True,
        opacity=1.0,
        auto_highlight=True
    )

    # create a Pydeck Deck with a map style that doesn't require a token
    # set the viewport location - slightly zoom out to ensure data is visible
    view_state = pdk.ViewState(
        latitude=mean_lat,
        longitude=mean_lon,
        zoom=11,  # Zoomed in more to see streets better
        pitch=0
    )

    # create a Pydeck Deck with the layer and view_state
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',  # Open source style
        tooltip={"html": "<b>{name}</b><br>Year: {year}<br>Cost: {cost}<br>Category: {category}<br>Description: {description} <br>Ward: {ward} <br>Alderman: {alderman} <br>Calls: {calls} <br>Number of Projects: {num_projects}"}
    )
    output_fp = pathlib.Path.cwd() / 'gitmoney/visualizations/gitmoney_map.html'
    
    # save the deck to an HTML file for direct viewing
    deck.to_html(output_fp, open_browser=False)

def main():
    # Load the data
    geo_mm_df = create_data_df()
       
    create_visualization(geo_mm_df)


if __name__ == "__main__":
    main()
