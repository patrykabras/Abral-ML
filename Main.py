import tensorflow as tf
import keras as ks
import numpy as np
import pandas as pd

# Make pandas DataFrames display all columns (or specific value instead of none)
pd.set_option('display.max_columns', None)

# Make pandas DataFrames display all rows (or specific value instead of none)
# pd.set_option('display.max_rows', None)

# Change pandas DataFrames width
pd.set_option('display.width', 1000)

# Define column names
headings = ['SHIPMENT_IDENTCODE', 'SHIPMENT_CREATEDATE', 'FIRST_EVENT', 'LAST_EVENT', 'RECEIVER_ZIP',
            'RECEIVER_COUNTRY_IOS2', 'SENDER_ZIP', 'SENDER_COUNTRY_IOS2', 'SHIPMENT_WEIGHT', 'CONTRACT_TYPE',
            'XLIDENTIFIER']

# Define values data types by converters
converters = {'SHIPMENT_CREATEDATE': lambda x: pd.to_datetime(x, errors='coerce'),
          'FIRST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
          'LAST_EVENT': lambda x: pd.to_datetime(x, errors='coerce'),
          'SHIPMENT_WEIGHT': lambda x: pd.to_numeric(x, errors='coerce')}

print("Start reading raport file")

# Read file including column names to achieve correctly formatted columns
df = pd.read_fwf("Data/tracking_data.rpt", skiprows=[1], names=headings, converters=converters, nrows=100000)

# Delete first row (column names read from file) to avoid double headers
df = df.iloc[1:]

print("Done!")

# Drop rows with Nan values in some columns
df = df.dropna()

# Check data types of DataFrame
# print(df.dtypes)

# Print header of DataFrame
# print(df.head)

# Print the whole DataFrame
print(df)

# print specific row of DataFrame
# print(df['RECEIVER_ZIP'])

# Export data to csv in order to check what exactly happend
# df.to_csv(r'Data/cos2.csv', sep=";", index=False)
