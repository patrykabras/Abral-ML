import math
import tensorflow as tf
import numpy as np


class NearestNeighbour:
    def __init__(self):
        pass

    def slice_data(self, data: np, train_data_percentage: int):
        # Randomly shuffle data (only rows are shuffled, columns stay the same)
        np.random.shuffle(data)

        # data should be 2D so we can specify rows and columns
        rows_number = data.shape[0]
        columns_number = data.shape[1]

        # calculate how much rows do we have for each dataset
        train_rows_number = math.floor(rows_number * (train_data_percentage / 100))
        test_rows_number = rows_number - train_rows_number

        # slice data into train and test datasets
        train_dataset = tf.slice(data, [0, 0], [train_rows_number, columns_number])
        test_dataset = tf.slice(data, [train_rows_number, 0], [test_rows_number, 2])

        print("train_dataset shape: ")
        print(train_dataset.shape)
        print("test_dataset shape: ")
        print(test_dataset.shape)
