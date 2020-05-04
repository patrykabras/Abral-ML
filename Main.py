# import tensorflow as tf
# import keras as ks
# import numpy as np
# import pandas as pd
from data_db_connector.DBLogic import DBLogic
from data_db_connector.DBConnector import DBConnector

dbc = DBConnector()
dbl = DBLogic(dbc)
dbl.initialize()
