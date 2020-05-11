import matplotlib.pyplot as plt
import numpy


class BasePlots:
    @staticmethod
    def distance_to_time(data: numpy):
        x = data[:, 0]
        y = data[:, 1]
        plt.plot(x, y, 'ro')
        plt.xlabel('time [s]')
        plt.ylabel('distance [km]')
        plt.show()
