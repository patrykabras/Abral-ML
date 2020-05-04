import pandas as pd
from data_logic.SingleRecord import SingleRecord


class ReadRpt:
    def __init__(self, path: str, rows: int = None, skip: int = None) -> None:
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
                self.df = pd.read_fwf(path, names=headings)
            else:
                self.df = pd.read_fwf(path, names=headings, skiprows=range(2, skip))
        else:
            if skip is None:
                self.df = pd.read_fwf(path, names=headings, nrows=rows)
            else:
                self.df = pd.read_fwf(path, names=headings, nrows=rows, skiprows=range(2, skip))

        # Delete first row (column names read from file) to avoid double headers
        self.df = self.df.iloc[2:]

        # Drop rows with Nan values
        self.df = self.df.dropna()

        for index, row in self.df.iterrows():
            sr = SingleRecord(row['SHIPMENT_IDENTCODE'], row['SHIPMENT_CREATEDATE'], row['FIRST_EVENT'],
                              row['LAST_EVENT'], row['RECEIVER_ZIP'], row['RECEIVER_COUNTRY_IOS2'], row['SENDER_ZIP'],
                              row['SENDER_COUNTRY_IOS2'], row['CONTRACT_TYPE'], row['XLIDENTIFIER'])
            # insert_sr_into_db(sr)

    def rows_info(self) -> None:
        print("Amount of Rows: " + str(len(self.df)))

    def export_to_csv(self, path: str) -> None:
        self.df.to_csv(path, sep=";", index=False)

    def print_column(self, column_name: str) -> None:
        print(self.df[column_name])

    def print_data_frame_info(self) -> None:
        print(self.df.dtypes)
        print(self.df)
