import math

import sklearn
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier


class NearestNeighbour:

    def __init__(self, data: np):
        self.data = data

    def slice_data(self, train_data_percentage: int):
        # Randomly shuffle data (only rows are shuffled, columns stay the same)
        np.random.shuffle(self.data)

        # data should be 2D so we can specify rows and columns
        rows_number = self.data.shape[0]
        columns_number = self.data.shape[1]

        # calculate how much rows do we have for each dataset
        train_rows_number = math.floor(rows_number * (train_data_percentage / 100))
        test_rows_number = rows_number - train_rows_number

        # slice data into train and test datasets
        train_dataset = tf.slice(self.data, [0, 0], [train_rows_number, columns_number])
        test_dataset = tf.slice(self.data, [train_rows_number, 0], [test_rows_number, 2])

        print("train_dataset shape: ")
        print(train_dataset.shape)
        print("test_dataset shape: ")
        print(test_dataset.shape)
        return train_dataset, test_dataset

    def predict(X_t, y_t, x_t, k_t):
        neg_one = tf.constant(-1.0, dtype=tf.float64)
        # we compute the L-1 distance
        distances = tf.reduce_sum(tf.abs(tf.subtract(X_t, x_t)), 1)
        # to find the nearest points, we find the farthest points based on negative distances
        # we need this trick because tensorflow has top_k api and no closest_k or reverse=True api
        neg_distances = tf.multiply(distances, neg_one)
        # get the indices
        vals, indx = tf.nn.top_k(neg_distances, k_t)
        # slice the labels of these points
        y_s = tf.gather(y_t, indx)
        return y_s

    def get_label(preds):
        counts = np.bincount(preds.astype('int64'))
        return np.argmax(counts)
