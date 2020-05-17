import pickle
import math
from sklearn import linear_model, preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
import sklearn
import numpy


class MachineLearning:

    def __init__(self):
        pass

    def epochML(self, epoch, records: numpy, accgap: float = 0):
        bestACCnow = accgap
        for x in range(0, epoch):
            x_train, x_test, y_train, y_test = self.splitData(records)
            model = KNeighborsClassifier(n_neighbors=100, weights='distance')
            model.fit(x_train, y_train)
            acc = model.score(x_test, y_test)
            if acc > bestACCnow:
                print(acc)
                bestACCnow = acc
                filename = 'Models/BestModel{}.sav'.format(acc)
                pickle.dump(model, open(filename, 'wb'))

    def kNeighbors(self, records: numpy):
        x_train, x_test, y_train, y_test = self.splitData(records)
        print("model after split")

        model = KNeighborsClassifier(n_neighbors=100, weights='distance')
        model.fit(x_train, y_train)
        print("model after train")

        acc = model.score(x_test, y_test)
        print(acc)

        self.printPredictResults(model, x_test, y_test)

        filename = 'Models/TestKnnSave.sav'
        pickle.dump(model, open(filename, 'wb'))

    def splitData(self, records: numpy):
        X = list(zip(records[:, 1], records[:, 2], records[:, 3], records[:, 4], records[:, 5], records[:, 6]))
        y = list(records[:, 0])
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)
        return x_train, x_test, y_train, y_test

    def loadModel(self, filename):
        return pickle.load(open(filename, 'rb'))

    def testSaveModel(self, filename, records):
        x_train, x_test, y_train, y_test = self.splitData(records)
        model = self.loadModel("Models/"+filename)
        acc = model.score(x_test, y_test)
        self.printPredictResults(model, x_test, y_test)
        print("Accuracy from sklearn.score() method = ", acc)

    def printPredictResults(self, model, x_test, y_test):
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
