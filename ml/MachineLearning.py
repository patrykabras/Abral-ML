import math
import pickle
from typing import Tuple

import numpy
import sklearn
from sklearn.neighbors import KNeighborsClassifier

from plots.BasePlots import BasePlots


class MachineLearning:

    def __init__(self):
        pass

    def epoch_ml(self, epoch, records: numpy, accgap: float = 0) -> None:
        best_acc_now = accgap
        for x in range(0, epoch):
            x_train, x_test, y_train, y_test = self.split_data(records)
            model = KNeighborsClassifier(n_neighbors=100, weights='distance')
            model.fit(x_train, y_train)
            acc = model.score(x_test, y_test)
            if acc > best_acc_now:
                print(acc)
                best_acc_now = acc
                filename = 'Models/BestModel{}.sav'.format(acc)
                pickle.dump(model, open(filename, 'wb'))

    def k_neighbors(self, records: numpy) -> None:
        x_train, x_test, y_train, y_test = self.split_data(records)
        print("Model after split.")

        model = KNeighborsClassifier(n_neighbors=100, weights='distance')
        model.fit(x_train, y_train)
        print("Model after train.")

        acc = model.score(x_test, y_test)
        print(acc)

        self.print_predict_results(model, x_test, y_test)

        BasePlots.occurrences_delivery_time_plot(records)
        filename = 'Models/TestKnnSave.sav'
        pickle.dump(model, open(filename, 'wb'))

    @staticmethod
    def split_data(records: numpy) -> Tuple[list, list, list, list]:
        X = list(zip(records[:, 1], records[:, 2], records[:, 3], records[:, 4], records[:, 5], records[:, 6]))
        y = list(records[:, 0])
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)
        print(type(x_train), ", ", type(x_train), ", ", type(x_train), ", ", type(x_train))
        return x_train, x_test, y_train, y_test

    @staticmethod
    def load_model(filename) -> pickle:
        return pickle.load(open(filename, 'rb'))

    def test_save_model(self, filename, records) -> None:
        x_train, x_test, y_train, y_test = self.split_data(records)
        model = self.load_model("Models/" + filename)
        acc = model.score(x_test, y_test)
        self.print_predict_results(model, x_test, y_test)
        print("Accuracy from sklearn.score() method = ", acc)

    @staticmethod
    def print_predict_results(model, x_test, y_test) -> None:
        prediction = model.predict(x_test)

        epsilon = 12  # number of hours
        correct_predictions = 0
        all_predictions = 0

        for x in range(len(prediction)):
            if math.fabs(prediction[x] - y_test[x]) < epsilon:
                correct_predictions = correct_predictions + 1
            all_predictions = all_predictions + 1
            # print("The difference is: |", prediction[x], " - ", y_test[x],
            #       "| = {:.2f}".format(math.fabs(prediction[x] - y_test[x])))
            print("Predicted: ", prediction[x], "Data: ", x_test[x], "Actual: ", y_test[x])

        print("\nSelf made accuracy calculators:")
        print("Prediction is classified as correct when belongs to range: ")
        print("from actual_value - {}h to actual_value + {}h".format(epsilon, epsilon))
        print("Classification accuracy = ", correct_predictions / all_predictions)
