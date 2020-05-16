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

    def random_test(self):
        amount_of_data = 800000
        le = preprocessing.LabelEncoder()

        time_label = le.fit_transform(list(records[:, 0]))

        distance = le.fit_transform(list(records[:, 2]))

        X = list(zip(records[:, 1], records[:, 2]))
        y = list(records[:, 0])

        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.30)
        model = KNeighborsClassifier(n_neighbors=100, weights='distance')
        model.fit(x_train, y_train)
        acc = model.score(x_test, y_test)

        correct_predictions = 0
        all_predictions = 0
        epsilon = 12  # number of hours
        prediction = model.predict(x_test)

        for x in range(len(prediction)):
            if math.fabs(prediction[x] - y_test[x]) < epsilon:
                correct_predictions = correct_predictions + 1
            all_predictions = all_predictions + 1
            print("The difference is: |", prediction[x], " - ", y_test[x],
                  "| = {:.2f}".format(math.fabs(prediction[x] - y_test[x])))
            # print("Predicted: {:.2f}".format(predicted[x]), "Data: ", x_test[x], "Actual: {:.2f}".format(y_test[x]))

        print("Accuracy from sklearn.score() method = ", acc)

        # What is the problem?
        # The main problem is that we dont't have clear output like yes/no, true/false, 1/0. We have an output of time...
        #
        # Even if we rounded input time values to hours it's still big amount of possible inputs.
        # In fact, when we are using KNeighborsRegressor the amount of possible outputs isn't even finite.
        # However, when we are using KNeighborsClassifier the amount of possible outputs is totally depending on the dataset
        # (amount of possible outputs is the same as amount of unique inputs).
        #
        # So yeah, in the moment of writing it we have about 695 different inputs (unix_differences) provided to the algorithm.

        print("\nSelf made accuracy calculators:")
        print("Prediction is classified as correct when belongs to range: ")
        print("from actual_value - {}h to actual_value + {}h".format(epsilon, epsilon))
        print("Classification accuracy = ", correct_predictions / all_predictions)
        print(
            "Logarithmic Loss accuracy cannot be calculated, because we dont have finite amount of possible events = ")
        print("Amount of unique unix_difference values: ", np.unique(records[:, 0]).shape[0])

        # predictions as 0 to 1 in 0.01 increments
        uniques = np.unique(records[:, 0])
        uniques_amount = uniques.shape[0]
        uniques_counter = np.zeros((uniques_amount,))
        uniques_proba = np.zeros((uniques_amount, 2))
        for i in range(uniques_amount):
            for cell in np[:, 0]:
                if cell == uniques[i]:
                    uniques_counter[i] = uniques_counter[i] + 1
            uniques_proba[i, 1] = uniques[i]
            uniques_proba[i, 0] = uniques_counter[i] / amount_of_data
            # print("There is ", uniques_counter[i], " values like: ", uniques[i], "h, so the probability is: ", uniques_proba[i, 0], "%")

        print(uniques_proba)

        # plt.hist(uniques_proba, density=True, bins=10, label="Data")
        highest_value = np.amax(uniques)
        xtics = np.zeros((11,))
        for i in range(11):
            xtics[i] = math.floor((highest_value / 10) * i)

        print(highest_value)
        plt.bar(uniques_proba[:, 1], uniques_counter, alpha=0.5)
        plt.xticks(xtics, xtics)
        plt.ylabel('Occurrences in DataSet')
        plt.xlabel('Delivery time [h]')
        plt.title('Probability for each unique delivery time hour')

        plt.show()