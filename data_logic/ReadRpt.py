import threading
import time
from threading import BoundedSemaphore

import pandas as pd

from data_db_connector.DBConnector import DBConnector
from data_logic.SingleRecord import SingleRecord
from db_tables.Completed_Table import Completed_Table
from db_tables.Contract_type_Table import Contract_type_Table
from db_tables.Missing_postcode_Table import Missing_postcode_Table
from db_tables.Postcode_Table import Postcode_Table


class ReadRpt:
    def __init__(self, threads_count: int) -> None:
        # Create main DBConnector and create connections pool and semaphores pool
        # to make it possible to work on multiple Thread
        self.dbc = DBConnector()
        self.cnx_pool = self.dbc.create_connection(32)
        self.semaphores_pool = BoundedSemaphore(value=threads_count)
        self.df = pd.DataFrame()

        # Define instances of main classes, pass the connection pool to them
        self.completed_table = Completed_Table(self.cnx_pool)
        self.contract_type_table = Contract_type_Table(self.cnx_pool)
        self.missing_postcode_table = Missing_postcode_Table(self.cnx_pool)
        self.postcode_table = Postcode_Table(self.cnx_pool)

        # Define column names
        self.headings = ['SHIPMENT_IDENTCODE', 'SHIPMENT_CREATEDATE', 'FIRST_EVENT', 'LAST_EVENT', 'RECEIVER_ZIP',
                         'RECEIVER_COUNTRY_IOS2', 'SENDER_ZIP', 'SENDER_COUNTRY_IOS2', 'SHIPMENT_WEIGHT',
                         'CONTRACT_TYPE', 'XLIDENTIFIER']

    def read(self, path: str, rows: int = None, skip: int = None) -> None:
        # Read file including column names to achieve correctly formatted columns
        # use skiprows=range(x,y) to skip specific range
        # use converters=x to set data converters for specific columns
        # use nrows=x to specify the number of rows to read

        print("\n--- Start reading RPT file. ---")
        reading_start_time = time.time()

        if rows is None:
            if skip is None:
                self.df = pd.read_fwf(path, names=self.headings, skiprows=1)
            else:
                self.df = pd.read_fwf(path, names=self.headings, skiprows=range(1, skip))
        else:
            if skip is None:
                self.df = pd.read_fwf(path, names=self.headings, nrows=rows, skiprows=1)
            else:
                self.df = pd.read_fwf(path, names=self.headings, nrows=rows, skiprows=range(1, skip))

        # Delete second row (column names read from file) to avoid double headers
        self.df = self.df.iloc[2:]

        # Drop rows with Nan values
        self.df = self.df.dropna(
            subset=['SHIPMENT_CREATEDATE', 'FIRST_EVENT', 'LAST_EVENT', 'RECEIVER_ZIP', 'SENDER_ZIP'])

        # Get names of indexes for which column RECEIVER_COUNTRY_IOS2 has value different than PL
        self.df = self.df[self.df['RECEIVER_COUNTRY_IOS2'] == 'PL']

        # Get names of indexes for which column RECEIVER_COUNTRY_IOS2 has value different than PL
        self.df = self.df[self.df['SENDER_COUNTRY_IOS2'] == 'PL']

        print(self.df)
        print("\n--- File reading completed in %s seconds. ---" % (time.time() - reading_start_time))
        print("\n--- File has been loaded and prepared for further operations. ---")

    def insert_data(self) -> None:
        if not self.df.empty:
            print("\n--- Start inserting into DB. ---")
            inserting_start_time = time.time()

            # iterate through each row of chosen data and insert it to DB simultaneously in multiple threads
            for index, row in self.df.iterrows():
                self.semaphores_pool.acquire()
                thread = threading.Thread(target=self.handle_single_row, args=(row,))
                thread.start()

            print("\n--- Data inserting completed in %s seconds. ---" % (time.time() - inserting_start_time))
        else:
            print("\n--- No data to work with. Use read() method to selected data. ---")

    def handle_single_row(self, row) -> None:
        # Create SingleRecord object and fill all his attributes by main constructor
        sr = SingleRecord(self.postcode_table, row['SHIPMENT_IDENTCODE'], row['SHIPMENT_CREATEDATE'], row['FIRST_EVENT'],
                          row['LAST_EVENT'], row['RECEIVER_ZIP'], row['RECEIVER_COUNTRY_IOS2'], row['SENDER_ZIP'],
                          row['SENDER_COUNTRY_IOS2'], row['CONTRACT_TYPE'], row['XLIDENTIFIER'])

        # Collect contract type id of created object from contract_type table
        contract_type_id = self.contract_type_table.get_contract_type_id(row['CONTRACT_TYPE'], row['XLIDENTIFIER'])

        if sr.receiver_zip_found and sr.sender_zip_found:
            # both zips need to be translated into coords in order to
            # calculate distance and insert record to complete table
            self.completed_table.insert_record(sr, contract_type_id)
        else:
            self.missing_postcode_table.handle_missing_record(sr)
        self.semaphores_pool.release()

    def rows_info(self) -> None:
        print("Amount of Rows: " + str(len(self.df)))

    def export_to_csv(self, path: str) -> None:
        self.df.to_csv(path, sep=";", index=False)

    def print_column(self, column_name: str) -> None:
        print(self.df[column_name])

    def print_data_frame_info(self) -> None:
        print(self.df.dtypes)
        print(self.df)
