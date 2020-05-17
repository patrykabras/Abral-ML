import math

import matplotlib.pyplot as plt
import numpy


class BasePlots:
    @staticmethod
    def distance_time_plot(data: numpy):
        x = data[:, 0]
        y = data[:, 1]
        plt.plot(x, y, 'ro')
        plt.xlabel('time [s]')
        plt.ylabel('distance [km]')
        plt.show()

    @staticmethod
    def occurrences_delivery_time_plot(data: numpy):
        amount_of_data = data.shape[0]
        print("Amount of unique unix_difference values: ", numpy.unique(data[:, 0]).shape[0])

        uniques = numpy.unique(data[:, 0])
        uniques_amount = uniques.shape[0]
        uniques_counter = numpy.zeros((uniques_amount,))
        uniques_proba = numpy.zeros((uniques_amount, 2))
        for i in range(uniques_amount):
            for cell in data[:, 0]:
                if cell == uniques[i]:
                    uniques_counter[i] = uniques_counter[i] + 1
            uniques_proba[i, 1] = uniques[i]
            uniques_proba[i, 0] = uniques_counter[i] / amount_of_data
            # print("There is ", uniques_counter[i], " values like: ", uniques[i], "h, so the probability is: ", uniques_proba[i, 0], "%")

        highest_value = numpy.amax(uniques)
        xtics = numpy.zeros((11,))
        for i in range(11):
            xtics[i] = math.floor((highest_value / 10) * i)

        plt.bar(uniques_proba[:, 1], uniques_counter, alpha=0.5)
        plt.xticks(xtics, xtics)
        plt.ylabel('Occurrences in DataSet')
        plt.xlabel('Delivery time [h]')
        plt.title('Occurrences of each unique delivery time hour [{}]'.format(amount_of_data))
        plt.show()
