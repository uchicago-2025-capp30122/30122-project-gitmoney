import pandas as pd
import geopandas as gpd
import shapely.wkt
import pathlib

if __name__ == '__main__':
    streets_ofp = pathlib.Path.cwd() / 'data/streets.geojson'
    streets_csv = pathlib.Path.cwd() / 'data/streets.csv' 
    streets_df = pd.read_csv(streets_csv)
    streets_df['geometry'] = streets_df['the_geom'].apply(shapely.wkt.loads)
    streets_gdf = gpd.GeoDataFrame(streets_df, geometry='geometry')
    streets_gdf.crs = 'EPSG:4326'
    streets_gdf.to_file(streets_ofp, driver="GeoJSON")
    streets_ofp = pathlib.Path.cwd() / 'data/streets.geojson' 