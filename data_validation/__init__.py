import pandas as pd


def read_rpt_file(path: str, rows: int) -> pd.DataFrame:
    # Define column names
    headings = ['SHIPMENT_IDENTCODE', 'SHIPMENT_CREATEDATE', 'FIRST_EVENT', 'LAST_EVENT', 'RECEIVER_ZIP',
                'RECEIVER_COUNTRY_IOS2', 'SENDER_ZIP', 'SENDER_COUNTRY_IOS2', 'SHIPMENT_WEIGHT', 'CONTRACT_TYPE',
                'XLIDENTIFIER']

    # Define values data types by converters
    converters = {'SHIPMENT_CREATEDATE': lambda x: pd.to_datetime(x, errors='coerce'),
                  'FIRST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
                  'LAST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
                  'SHIPMENT_WEIGHT': lambda x: pd.to_numeric(x, errors='coerce')}

    # Read file including column names to achieve correctly formatted columns
    df = pd.read_fwf(path, skiprows=[1], names=headings, converters=converters, nrows=rows)

    # Delete first row (column names read from file) to avoid double headers
    df = df.iloc[1:]

    # Drop rows with Nan values in some columns
    df = df.dropna()

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


def get_eval_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.iloc[round((len(df) * 70) / 100):]


def get_train_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[:round((len(df) * 70) / 100)]
