#### Data Visualization

import pandas as pd
import pathlib

import shapely.wkt
import polars as pl
import geopolars as gpl
import geopandas as gpd
import plotly.graph_objects as go
import json
import shapely
import numpy as np
import plotly.express as px
import ast



if __name__ == "__main__":
    mm_csv = pathlib.Path.cwd() / 'data/final_menu_money.csv' 
    streets_csv = pathlib.Path.cwd() / 'data/streets.csv' 
    mm_df = pd.read_csv(mm_csv).drop_duplicates()
    streets_df = pd.read_csv(streets_csv)
    streets_df['geometry'] = streets_df['the_geom'].apply(shapely.wkt.loads)
    streets_gdf = gpd.GeoDataFrame(streets_df, geometry='geometry')
    streets_gdf.crs = 'EPSG:4326'
    geo_mm_df = streets_df.join(mm_df,
                           on='OBJECTID',
                           how='inner',
                           lsuffix='_st',
                           rsuffix='_mm')
    lats = []
    lons = []
    names = []
    years = []
    costs = []
    categories = []
    descriptions = []

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
        for linestring in linestrings:
            x, y = linestring.xy
            lats = np.append(lats, y)
            lons = np.append(lons, x)
            names = np.append(names, [name]*len(y))
            years = np.append(years, [year]*len(y))
            costs = np.append(costs, [cost]*len(y))
            categories = np.append(categories, [category]*len(y))
            descriptions = np.append(descriptions, [description]*len(y))
            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            years = np.append(years, None)
            costs = np.append(costs, None)
            categories = np.append(categories, None)
            descriptions = np.append(descriptions, None)

    fig = px.line_map(lat=lats, lon=lons, hover_name=names,
                      hover_data={'year': years, 'cost': costs, 'category': categories, 'description': descriptions},
                      map_style="open-street-map", zoom=10)
    fig.show()