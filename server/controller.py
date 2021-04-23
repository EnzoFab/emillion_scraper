import numpy as np
from business import business


class Controller():
    """

    """

    def __init__(self):
        pass

    def get_histogram(self, htype: int):
        """
            get histogram according to the type
            htype: 0 or 1
                - 0: numbers
                - 1: stars
        """

        if htype == 0:
            return self.__histogram(business.numbers_flat).tolist()

        return self.__histogram(business.stars_flat).tolist()

    def __histogram(self, d2_array):

        (unique, counts) = np.unique(d2_array, return_counts=True)

        return np.asarray((unique, counts)).T

    def get_random_draw(self, count: int):
        """
            Generate $(count) random draw to play euromillion
        """

    def get_last_draw(self, number):
        """  """


controller = Controller()
