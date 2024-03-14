from math import sin, cos
from numpy import deg2rad
import pandas as pd
import geopy.distance as gp_dist  # Install geopy: pip install geopy


def lat_lon_distance(lat1, lon1, lat2, lon2):
    """ Calculate the distance between two point
    :param lat1: Latitude of first point
    :param lon1: Longitude of first point
    :param lat2: Latitude of second point
    :param lon2: Longitude of second point
    :return: Distance between two points in kilometer(km)"""
    try:
        delta_lat = deg2rad(lat2 - lat1)
        delta_lon = deg2rad(lon2 - lon1)
    except ValueError:
        print(lat1, lon1, lat2, lon2)

    line = (sin(delta_lat / 2) * cos(delta_lat / 2) + cos(lat1) * sin(delta_lat / 2) +
            cos(deg2rad(lat1)) * cos(deg2rad(lat2)) * sin(delta_lat / 2) * cos(delta_lon / 2))
    return line * gp_dist.EARTH_RADIUS


def convert_gtfs_to_csv(gtfs_dir,
                        output_col=None):
    """
    Converts GTFS files from a directory to a CSV with stops and passing lines, with potential transferability information,
    including origin stop ID (current stop) and destination stop ID (next stop).

    Args:
      gtfs_dir (str): Path to the directory containing GTFS files.
      transfer_distance_threshold (float, optional): Maximum distance between stops considered transferable. Defaults to 500 meters.

    Returns:
      None
    """

    if output_col is None:
        output_col = ['stop_id', 'stop_name', 'agency_id',
                      'route_id', 'route_short_name', 'next_stop_id']
    try:
        # Read GTFS files
        stops_df = pd.read_csv(f"{gtfs_dir}/stops.txt")
        routes_df = pd.read_csv(f"{gtfs_dir}/routes.txt")
        stop_times_df = pd.read_csv(f"{gtfs_dir}/stop_times.txt")
        trips_df = pd.read_csv(f"{gtfs_dir}/trips.txt")
        # Merge DataFrames
        merged_df = stop_times_df.merge(stops_df[['stop_id', 'stop_name']], how='left',
                                        on='stop_id')
        merged_df = merged_df.merge(trips_df[['trip_id', 'route_id']], how='left', on='trip_id')

        merged_df = merged_df.merge(routes_df[['route_id', 'route_short_name', 'agency_id']], how='left', on='route_id')

        def fill_missing_route_id(row):
            if pd.isna(row['route_id']):
                trip_id = row['trip_id']
                trip_ls = trips_df['trip_id'].tolist()
                trip_ind = trip_ls.index(str(trip_id).strip())
                trip_ls = trips_df['route_id'].tolist()
                return trip_ls[trip_ind]

        merged_df['route_id'] = merged_df.apply(fill_missing_route_id, axis=1)

        # Calculate the next stop ID (considering the last stop has None as next)
        merged_df['next_stop_id'] = merged_df.groupby('trip_id')['stop_id'].transform(lambda x: x.shift(-1))

        # Select and format output columns
        output_df = merged_df[output_col]

        # Sort only if stop_sequence is available
        if 'stop_sequence' in output_df.columns:
            output_df = output_df.sort_values(by=['route_short_name', 'stop_sequence'], na_position='last')

        # Rename columns for clarity (optional)
        output_df = output_df.rename(columns={'stop_id': 'origin_id', 'next_stop_id': 'dest_id'})

        # Export to CSV
        output_df.to_csv(f'{gtfs_dir}_stop_line.csv', index=False)

        print(f"Conversion successful! Output saved to {gtfs_dir}_stop_line.csv")

    except FileNotFoundError as e:
        print(f"Error: GTFS files not found in directory {gtfs_dir}. Please check the path.")
    except pd.errors.ParserError as e:
        print(f"Error: Invalid GTFS file format. Please ensure the files are in valid GTFS format.")
    except KeyError as e:
        print(f"Error: Missing column '{e.args[0]}' in GTFS data. Please check your data structure.")


if __name__ == "__main__":
    convert_gtfs_to_csv('fairbank', output_col=['stop_id', 'route_id', 'next_stop_id'])

