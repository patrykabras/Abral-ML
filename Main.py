#import tensorflow as tf
# import keras as ks
# import numpy as np
# import pandas as pd
import math
import time
from asyncio import BoundedSemaphore

import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier


from data_db_connector.DBLogic import DBLogic
from data_db_connector.DBConnector import DBConnector
from data_logic.SingleRecord import SingleRecord
from db_tables.Completed_Table import Completed_Table
from db_tables.Contract_type_Table import Contract_type_Table
from db_tables.Missing_postcode_Table import Missing_postcode_Table
from db_tables.Postcode_Table import Postcode_Table
from data_logic.ReadRpt import ReadRpt

# Create database structure if needed
# dbc = DBConnector(True)
# dbl = DBLogic(dbc)
# dbl.initialize()

# Fill postcode_table (which is dictionary table for zip codes translating) with data from file.
# dbc = DBConnector()
# cnx = dbc.create_connection(32)
# pct = Postcode_Table(cnx)
# pct.fill_table("Data/PL.txt")

# Mock for coords testing
# coordReturn = pct.getCoordinates("PL", "68-30660")
# print("empty : ", coordReturn.get("empty"))
# if coordReturn.get("empty"):
#     print("empty true")
# else:
#     print("empty false")

# Mock for single record insertion
# completed_table = Completed_Table(DBConnector())
# contract_type_table = Contract_type_Table(DBConnector())
# sr2 = SingleRecord('21768839059', '2020-02-21 03:49:36.620', '2020-02-21 22:20:00.000', '2020-02-24 02:53:00.000',
#                    '86-160', 'PL', '86-160', 'PL', 'DHL Parcel Polska', 'DHL-48')
# contract_type_id = contract_type_table.check_if_contract_type_exists('DHL Parcel Polska', 'DHL-48')
# if sr2.receiver_zip_found and sr2.sender_zip_found:
#     completed_table.insert_record(sr2, contract_type_id)
# else:
#     print("Missing data, record should be inserted into forth table")

# Important thing is that connection pool is always 32, so be aware to set your database
# to allow 32 connections (xampp mysql database is set up to 151 connections in default)

# threads_count = 5
# start_from = 2000000
# rows_count = 50000
#
# start_time = time.time()
# readRpt = ReadRpt(threads_count)
# readRpt.read("Data/tracking_data.rpt", rows_count, start_from)
# readRpt.insert_data()

# print("\n--- Program completed in %s seconds. ---" % (time.time() - start_time))

# Following lines of code lets you update dictionary table with missing zip codes (using geolocalization services)
# dbc = DBConnector()
# cnx_pool = dbc.create_connection(32)
# missing_postcodes = Missing_postcode_Table(cnx_pool)
# missing_postcodes.update_dictionary_with_missing_postcodes(10)

import numpy as np
import tensorflow as tf

from model.NearestNeighbour import NearestNeighbour
from plots import BasePlots as plt

print(tf.version)

# get data from DB
dbc = DBConnector()
cnx_pool = dbc.create_connection(32)

completed_table = Completed_Table(cnx_pool)
records = completed_table.collect_data(0, 100000)

from sklearn import linear_model, preprocessing

le = preprocessing.LabelEncoder()

time_label = le.fit_transform(list(records[:, 0]))

distance = le.fit_transform(list(records[:, 1]))

X = list(zip(records[:, 1]))
y = list(records[:, 0])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)

model = KNeighborsClassifier(n_neighbors=100)

model.fit(x_train, y_train)
acc = model.score(x_test, y_test)

print(acc)

predicted = model.predict(x_test)

for x in range(len(predicted)):
    print("Predicted: ", predicted[x], "Data: ", x_test[x], "Actual: ", y_test[x])
    # n = model.kneighbors([x_test[x]], 9, True)
    # print("N: ", n)