#### Data Visualization

import pandas as pd
import pathlib
import shapely.wkt
import geopandas as gpd
import pydeck as pdk
from dash import Dash, html
import numpy as np
import random
def explode_multilinestrings(gdf):
    new_rows = []
    for index, row in gdf.iterrows():
        if row['geometry'].geom_type == 'MultiLineString':
            for line in row['geometry'].geoms:
                new_rows.append({**row.to_dict(), 'geometry': line})
        else:
            new_rows.append(row.to_dict())
    return gpd.GeoDataFrame(new_rows, crs=gdf.crs)

if __name__ == "__main__":
    # Load the data
    mm_csv = pathlib.Path.cwd() / 'data/final_menu_money.csv' 
    streets_csv = pathlib.Path.cwd() / 'data/streets.csv' 
    mm_df = pd.read_csv(mm_csv).drop_duplicates()
    streets_df = pd.read_csv(streets_csv)
    
    # Convert the 'the_geom' column from WKT strings to geometry objects
    streets_df['geometry'] = streets_df['the_geom'].apply(shapely.wkt.loads)
    
    # Create a GeoDataFrame
    streets_gdf = gpd.GeoDataFrame(streets_df, geometry='geometry')
    streets_gdf.crs = 'EPSG:4326'
    
    # Perform the join operation
    geo_mm_df = streets_gdf.merge(mm_df,
                                  left_on='OBJECTID',
                                  right_on='OBJECTID',
                                  how='inner',
                                  suffixes=('_st', '_mm'))
    
    print(f"Merged dataframe size: {len(geo_mm_df)}")

    # Check if there is any data after the merge
    if len(geo_mm_df) == 0:
        print("No matching records found in the merge. Please check your data.")
        exit()

    # IMPORTANT: Make sure we're working with WGS84 (EPSG:4326) for web maps
    geo_mm_df = geo_mm_df.to_crs(epsg=4326)
    
    # Calculate mean latitude and longitude for the viewport
    mean_lat = geo_mm_df.geometry.centroid.y.mean()
    mean_lon = geo_mm_df.geometry.centroid.x.mean()
    
    print(f"Mean latitude: {mean_lat}, Mean longitude: {mean_lon}")

    # Prepare data for Pydeck - IMPORTANT: Ensure coordinates are in [longitude, latitude] format
    path_data = []
    for feature, name, year, cost, category, description in zip(geo_mm_df.geometry, geo_mm_df.description, geo_mm_df.year, geo_mm_df.cost, geo_mm_df.category, geo_mm_df.description):
        # Convert WKT string to geometry object if necessary
        if isinstance(feature, str):
            feature = shapely.wkt.loads(feature)
        
        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        
        # Change this section to use lists instead of tuples for coordinates
        for linestring in linestrings:
            # Get coordinates as LISTS instead of tuples, ensure they're in [longitude, latitude] format
            coords = [[float(lon), float(lat)] for lon, lat in zip(linestring.xy[0], linestring.xy[1])]
            if len(coords) >= 2:  # Only add if we have at least 2 coordinates (a valid line)
                path_data.append({
                    'path': coords,
                    'name': str(name),
                    'year': str(year),
                    'cost': str(cost),
                    'category': str(category),
                    'description': str(description)
                })

    # Debugging: Print the path data to verify
    print(f"Number of paths: {len(path_data)}")
    if path_data:
        print(f"Sample path: {path_data[0]['path'][:2]}")
        print(f"Full first path: {path_data[0]['path']}")
        
        # Check the bounds of the first path to make sure it's in a reasonable area
        min_lon = min(p[0] for p in path_data[0]['path'])
        max_lon = max(p[0] for p in path_data[0]['path'])
        min_lat = min(p[1] for p in path_data[0]['path'])
        max_lat = max(p[1] for p in path_data[0]['path'])
        print(f"Bounds of first path: lon: {min_lon} to {max_lon}, lat: {min_lat} to {max_lat}")

    layer = pdk.Layer(
        'PathLayer',
        data=path_data,
        get_path='path',
        get_color=[255, 0, 0, 255],
        get_width=10,  # Increased width for better visibility
        pickable=True,
        opacity=1.0,
        auto_highlight=True
    )
    
    # Set the viewport location - slightly zoom out to ensure data is visible
    view_state = pdk.ViewState(
        latitude=mean_lat,
        longitude=mean_lon,
        zoom=11,  # Zoomed in more to see streets better
        pitch=0
    )

    # Create a Pydeck Deck with a map style that doesn't require a token
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',  # Open source style
        tooltip={"html": "<b>{name}</b><br>Year: {year}<br>Cost: {cost}<br>Category: {category}<br>Description: {description}"}
    )

    # Save the deck to an HTML file for direct viewing
    deck.to_html('path_layer_direct.html', open_browser=True)
    
    # Also create the Dash app
    deck_html = deck.to_html(as_string=True)
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1("Chicago Streets Visualization"),
        html.Iframe(srcDoc=deck_html, width='100%', height='800px')
    ])

    # Run the Dash application
    app.run_server(debug=True)