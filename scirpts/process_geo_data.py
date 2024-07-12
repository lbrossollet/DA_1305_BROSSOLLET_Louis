import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import json
import os

def main():
    # Define file paths
    script_dir = os.path.dirname(__file__)  # Current directory of the script
    data_dir = os.path.join(script_dir, '../data_processed')
    traffic_data_geo_path = os.path.join(data_dir, 'traffic_data_geo.csv')
    quartier_data_path_csv = os.path.join(script_dir, '../data', 'quartier_paris.csv')
    unique_points_geojson_path = os.path.join(data_dir, 'traffic_data_geo.geojson')
    quartier_data_geojson_path = os.path.join(data_dir, 'quartier_paris.geojson')

    # Check file existence
    if not os.path.exists(traffic_data_geo_path):
        raise FileNotFoundError(f"File not found: {traffic_data_geo_path}")

    if not os.path.exists(quartier_data_path_csv):
        raise FileNotFoundError(f"File not found: {quartier_data_path_csv}")

    # Load traffic data (points)
    print(f"Loading traffic data from: {traffic_data_geo_path}")
    df_points = pd.read_csv(traffic_data_geo_path)
    print("Traffic data loaded.")

    # Load quartier data
    print("Loading quartier data...")
    df_quartiers = pd.read_csv(quartier_data_path_csv, sep=";")
    print("Quartier data loaded.")

    # Function to parse polygon coordinates from JSON string
    def parse_polygon(polygon_str):
        try:
            coordinates = json.loads(polygon_str)['coordinates'][0]
            coordinates = [(float(lon), float(lat)) for lon, lat in coordinates]
            return Polygon(coordinates)
        except Exception as e:
            print(f"Error parsing polygon: {e}")
            return None

    # Convert unique points coordinates to Point objects
    print("Converting unique points coordinates to Point objects...")
    df_points['geometry'] = df_points.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
    print("Conversion completed.")

    # Create GeoDataFrame for points
    print("Creating GeoDataFrame for points...")
    gdf_points = gpd.GeoDataFrame(df_points, geometry='geometry', crs='EPSG:4326')
    print("GeoDataFrame for points created.")

    # Convert quartier coordinates to Polygon objects
    print("Converting quartier coordinates to Polygon objects...")
    df_quartiers['geometry'] = df_quartiers['Geometry'].apply(parse_polygon)
    print("Conversion completed.")

    # Create GeoDataFrame for quartiers
    print("Creating GeoDataFrame for quartiers...")
    gdf_quartiers = gpd.GeoDataFrame(df_quartiers[['N_SQ_QU', 'C_QU', 'C_QUINSEE', 'L_QU', 'C_AR', 'N_SQ_AR', 'PERIMETRE', 'SURFACE', 'geometry']], geometry='geometry', crs='EPSG:4326')
    print("GeoDataFrame for quartiers created.")

    # Save GeoJSON files
    print("Saving GeoJSON files...")
    gdf_points.to_file(unique_points_geojson_path, driver="GeoJSON")
    gdf_quartiers.to_file(quartier_data_geojson_path, driver="GeoJSON")
    print("GeoJSON files saved.")

    # Check file existence for spatial join part
    if not os.path.exists(unique_points_geojson_path):
        raise FileNotFoundError(f"File not found: {unique_points_geojson_path}")

    if not os.path.exists(quartier_data_geojson_path):
        raise FileNotFoundError(f"File not found: {quartier_data_geojson_path}")

    # Load points and quartier data into GeoDataFrames
    gdf_points = gpd.read_file(unique_points_geojson_path)
    gdf_quartiers = gpd.read_file(quartier_data_geojson_path)

    # Spatial join to find which quartier each point belongs to
    gdf_points_with_quartiers = gpd.sjoin(gdf_points, gdf_quartiers, how="left", op='within')

    # Select relevant columns for output CSV
    df_output = gdf_points_with_quartiers[['Identifiant_arc', 'Latitude', 'Longitude', 'N_SQ_QU']]

    # Save as CSV
    output_csv_path = os.path.join(data_dir, 'df_unique_points_with_quartiers.csv')
    df_output.to_csv(output_csv_path, index=False)
    print(f"CSV file saved: {output_csv_path}")

    # Save as GeoJSON
    output_geojson_path = os.path.join(data_dir, 'df_unique_points_with_quartiers.geojson')
    gdf_points_with_quartiers.to_file(output_geojson_path, driver='GeoJSON')
    print(f"GeoJSON file saved: {output_geojson_path}")

if __name__ == "__main__":
    main()
