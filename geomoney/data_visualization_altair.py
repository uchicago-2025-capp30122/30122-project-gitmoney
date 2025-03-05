import pandas as pd
import geopandas as gpd
import shapely
import pathlib
import altair as alt
import numpy as np
from dash import Dash, html
import os
import vegafusion
import pydeck as pdk
import json
import requests

### Altair test

def create_points_df_from_lines(gdf):
    """Convert LineString/MultiLineString geometries to points for Altair."""
    points = []
    for idx, row in gdf.iterrows():
        geom = row.geometry
        if geom.geom_type == 'LineString':
            for x, y in geom.coords:
                points.append({
                    'lon': x,
                    'lat': y,
                    'year': row.year,
                    'cost': row.cost,
                    'category': row.category,
                    'description': row.description,
                    'segment_id': idx  # To identify which segments belong together
                })
        elif geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                for x, y in line.coords:
                    points.append({
                        'lon': x,
                        'lat': y,
                        'year': row.year,
                        'cost': row.cost,
                        'category': row.category,
                        'description': row.description,
                        'segment_id': idx  # To identify which segments belong together
                    })
    return pd.DataFrame(points)

def get_chicago_geojson():
    """Get Chicago boundaries GeoJSON for the basemap."""
    # Option 1: Download from a URL
    url = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/il_illinois_zip_codes_geo.min.json"
    try:
        response = requests.get(url)
        chicago_geojson = response.json()
        return chicago_geojson
    except:
        # Option 2: If download fails, return a basic GeoJSON with Chicago bounds
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"name": "Chicago"},
                    "geometry": {
                        "type": "Polygon", 
                        "coordinates": [[
                            [-87.94, 41.64], 
                            [-87.52, 41.64], 
                            [-87.52, 42.02], 
                            [-87.94, 42.02], 
                            [-87.94, 41.64]
                        ]]
                    }
                }
            ]
        }

if __name__ == "__main__":
    alt.data_transformers.disable_max_rows()
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
    
    # Convert the LineString/MultiLineString geometries to points for Altair
    points_df = create_points_df_from_lines(geo_mm_df)
    
    # Calculate the center of the map
    center_lon = points_df['lon'].mean()
    center_lat = points_df['lat'].mean()
    
        # Get Chicago GeoJSON for the basemap
    # Replace the basemap creation part with this code:

    # Get Chicago GeoJSON for the basemap
    chicago_geojson = get_chicago_geojson()

    # Save the GeoJSON to a file
    os.makedirs('data', exist_ok=True)
    with open('data/chicago_geojson.json', 'w') as f:
        json.dump(chicago_geojson, f)

        
    # Try a different approach for the basemap
    basemap = alt.Chart(
        alt.topo_feature('https://raw.githubusercontent.com/vega/vega-datasets/master/data/us-10m.json', 'counties')
    ).mark_geoshape(
        fill='lightgray',
        stroke='white',
        opacity=0.2
    ).project(
        type='mercator',
        scale=50000,
        center=[center_lon, center_lat]
    )

    # Create the base map for our data with proper configuration
    base = alt.Chart(points_df).encode(
        longitude='lon:Q',
        latitude='lat:Q'
    )

    # Create point layer
    points = base.mark_circle(size=10).encode(
        color=alt.Color('year:N', scale=alt.Scale(scheme='viridis')),
        tooltip=['description', 'year', 'cost', 'category']
    )

    # Connect points that belong to the same segment
    lines = base.mark_line(strokeWidth=3).encode(
        color=alt.Color('year:N', scale=alt.Scale(scheme='viridis')),
        detail='segment_id:N'  # Group by segment_id
    )

    # First, create the combined data visualization without the basemap
    data_viz = alt.layer(lines, points).project(
        type='mercator',
        scale=50000,
        center=[center_lon, center_lat]
    )

    # Now create the final chart with all components
    chart = alt.layer(
        basemap,
        data_viz
    ).properties(
        width=800,
        height=600,
        title='Chicago Streets Visualization'
    ).configure_view(
        strokeWidth=0
    )

    # Add interactivity with explicit parameters
    chart = chart.interactive()
    # Display the chart
    chart.save('chicago_streets_map.html')
    print("Map saved to chicago_streets_map.html")

    # Save the chart as HTML
    chart_html = chart.to_html()

    # Create a Dash application
    app = Dash(__name__)
    
    # Define the layout
    app.layout = html.Div([
        html.H1("Chicago Streets Visualization with Altair"),
        html.Div([
            html.P("This visualization shows Chicago streets by year. You can zoom by scrolling and pan by dragging."),
            html.P("Hover over the lines or points for more information.")
        ], style={'margin-bottom': '20px'}),
        html.Iframe(
            srcDoc=chart_html,
            style={"width": "100%", "height": "800px", "border": "none"}
        )
    ])
    
    # Run the application
    app.run_server(debug=True)