import tensorflow as tf
import keras as ks
import numpy as np
import pandas as pd
import data_validation as dv

df = dv.read_rpt_file('Data/tracking_data.rpt', 10000)
eval_df = dv.get_eval_df(df)  # 30%
train_df = dv.get_train_df(df)  # 70%

print(eval_df)
print(train_df)
