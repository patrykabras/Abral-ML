import tensorflow as tf
import keras as ks
import  numpy as np
import pandas as pd


df = pd.read_csv("Data/tracking_data.rpt", skiprows=[1], nrows=150)

print(df.head())
