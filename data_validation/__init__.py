import math
import time
import pandas as pd
from geopy import Nominatim, Point
from geopy.distance import distance
from geopy.extra.rate_limiter import RateLimiter


def read_rpt_file(path: str, rows: int = None, skip: int = None) -> pd.DataFrame:
    # Define column names
    headings = ['SHIPMENT_IDENTCODE', 'SHIPMENT_CREATEDATE', 'FIRST_EVENT', 'LAST_EVENT', 'RECEIVER_ZIP',
                'RECEIVER_COUNTRY_IOS2', 'SENDER_ZIP', 'SENDER_COUNTRY_IOS2', 'SHIPMENT_WEIGHT', 'CONTRACT_TYPE',
                'XLIDENTIFIER']

    # Define values data types by converters
    converters = {'SHIPMENT_CREATEDATE': lambda x: pd.to_datetime(x, errors='coerce'),
                  'FIRST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
                  'LAST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
                  'SHIPMENT_WEIGHT': lambda x: pd.to_numeric(x, errors='coerce')}

    converters1 = {'SHIPMENT_CREATEDATE': lambda x: pd.to_datetime(x, errors='coerce'),
                  'FIRST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
                  'LAST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
                  'SHIPMENT_WEIGHT': lambda x: pd.to_numeric(x, errors='coerce')}

    # Read file including column names to achieve correctly formatted columns
    # use skiprows=range(x,y) to skip specific range
    # use converters=x to set data converters for specific columns
    # use nrows=x to specify the number of rows to read
    if rows is None:
        if skip is None:
            df = pd.read_fwf(path, names=headings)
        else:
            df = pd.read_fwf(path, names=headings, skiprows=range(2, skip))
    else:
        if skip is None:
            df = pd.read_fwf(path, names=headings, nrows=rows)
        else:
            df = pd.read_fwf(path, names=headings, nrows=rows, skiprows=range(2, skip))

    # Delete first row (column names read from file) to avoid double headers
    df = df.iloc[2:]

    # Drop rows with Nan values in some columns
    df = df.dropna(subset=['SHIPMENT_CREATEDATE', 'FIRST_EVENT', 'LAST_EVENT', 'RECEIVER_ZIP', 'SENDER_ZIP'])

    return df


def rows_info(df: pd.DataFrame) -> None:
    print("Amount of Rows: " + str(len(df)))


def export_to_csv(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, sep=";", index=False)


def print_column(df: pd.DataFrame, column_name: str) -> None:
    print(df[column_name])


def print_data_frame_info(df: pd.DataFrame) -> None:
    print(df.dtypes)
    print(df)


def convert_receiver_zip_to_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    geolocator = Nominatim(user_agent="convert1")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    df["RECEIVER_LONGITUDE"] = df["RECEIVER_ZIP"].apply(
        lambda x: {"postalcode": '90-001'} if x == '90-000' else {"postalcode": x}).apply(geocode).apply(
        lambda x: [x.latitude, x.longitude] if x is not None else [None, None])
    df["RECEIVER_LATITUDE"] = df["RECEIVER_LONGITUDE"].str[0]
    df["RECEIVER_LONGITUDE"] = df["RECEIVER_LONGITUDE"].str[1]
    return df


def convert_sender_zip_to_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    geolocator = Nominatim(user_agent="convert2")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    df["SENDER_LONGITUDE"] = df["SENDER_ZIP"].apply(
        lambda x: {"postalcode": '90-001'} if x == '90-000' else {"postalcode": x}).apply(geocode).apply(
        lambda x: [x.latitude, x.longitude] if x is not None else [None, None])
    df["SENDER_LATITUDE"] = df["SENDER_LONGITUDE"].str[0]
    df["SENDER_LONGITUDE"] = df["SENDER_LONGITUDE"].str[1]
    return df


def convert_zips_to_distance(df: pd.DataFrame) -> pd.DataFrame:
    gelocator = Nominatim(user_agent="convert3")
    g = RateLimiter(gelocator.geocode, min_delay_seconds=2)

    df["DISTANCE"] = df.apply(lambda row: distance(
        (Point(latitude=g(row["SENDER_ZIP"]).latitude, longitude=g(row["SENDER_ZIP"]).longitude)),
        (Point(latitude=g(row["RECEIVER_ZIP"]).latitude, longitude=g(row["RECEIVER_ZIP"]).longitude))
    ).km, axis=1)
    return df


def convert_coordinates_to_distance(df: pd.DataFrame) -> pd.DataFrame:
    df["DISTANCE"] = df.apply(lambda row: distance(
        (Point(latitude=row["SENDER_LATITUDE"], longitude=row["SENDER_LONGITUDE"])),
        (Point(latitude=row["RECEIVER_LATITUDE"], longitude=row["RECEIVER_LONGITUDE"]))
    ).km if not math.isnan(row["SENDER_LATITUDE"]) and not math.isnan(row["RECEIVER_LATITUDE"]) else None, axis=1)
    return df


def convert_to_distance_test() -> None:
    pd.set_option('display.max_columns', None)

    # Make pandas DataFrames display all rows (or specific value instead of none)
    #pd.set_option('display.max_rows', None)

    # Change pandas DataFrames width
    pd.set_option('display.width', 1000)

    start_time = time.time()

    df = read_rpt_file('Data/tracking_data.rpt', None, 100)

    df = convert_zips_to_distance(df)
    print(df[["SENDER_ZIP", "RECEIVER_ZIP", "DISTANCE"]])

    # df = convert_sender_zip_to_coordinates(df)
    # print(df[["SENDER_ZIP", "SENDER_LATITUDE", "SENDER_LONGITUDE"]])
    #print("\n\n")

    # df = convert_receiver_zip_to_coordinates(df)
    # print(df[["RECEIVER_ZIP", "RECEIVER_LATITUDE", "RECEIVER_LONGITUDE"]])
    #print("\n\n")

    export_to_csv(df, "Data/100rekordow.csv")

    # df = convert_coordinates_to_distance(df)
    #print(df[["SENDER_ZIP", "SENDER_LATITUDE", "SENDER_LONGITUDE", "RECEIVER_ZIP", "RECEIVER_LATITUDE",
    #          "RECEIVER_LONGITUDE", "DISTANCE"]])
    #print("\n\n")

    print(df)

    print("--- %s seconds ---" % (time.time() - start_time))

    #export_to_csv(df, "Data/distance.csv")


def shit_testing(df: pd.DataFrame) -> None:
    geolocator = Nominatim(user_agent="6")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    df["GEOCODE"] = df["SENDER_ZIP"].apply(
        lambda x: {"postalcode": '90-001'} if x is "90-000" else {"postalcode": x}).apply(geocode)
    print(df[["SENDER_ZIP", "GEOCODE"]])
    print("\n\n")
