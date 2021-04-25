import pandas as pd
import numpy as np
from helper import prepare_arrays, string_to_array


class Business():
    """
        Class which reads and parses the data from the csv file
    """

    def __init__(self):
        self.__raw_data = pd.read_csv("../euro_million_history.csv")

        self.__raw_numbers = self.__raw_data["numbers"]
        self.__raw_stars = self.__raw_data["stars"]

    @property
    def numbers(self) -> np.array:
        """
            return a 2d-array of numbers representing the numbers
            an array composed of a list of arrays
                also composed by five different integers between 1 and 50
        """

        return prepare_arrays(self.__raw_numbers)

    @property
    def stars(self) -> np.array:
        """
            return a 2d-array of numbers representing the stars
            an array composed by list of pairs of two different integers between 1 and 12
        """

        return prepare_arrays(self.__raw_stars)

    @property
    def numbers_flat(self) -> np.array:
        """
            return a 1d-array out of the numbers property
        """

        return self.numbers.flatten()

    @property
    def stars_flat(self) -> np.array:
        """
            return a 1d-array out of the stars property
        """

        # can also use flatten
        return self.stars.reshape((self.stars.size, 1))

    def generate_random_draw(self):
        """
            Generate a random draw
        """

        numbers = np.arange(1, 50)
        stars = np.arange(1, 12)

        r_numbers = np.random.choice(numbers, 5, replace=False)
        r_stars = np.random.choice(stars, 2, replace=False)

        return {"numbers": r_numbers.tolist(), "stars": r_stars.tolist()}

    @property
    def draws(self) -> np.array:
        """
            return a 1d-array composed by dict.
            each dict contains the result of a draw.
        """

        def func(row):
            numbers = string_to_array(row["numbers"])
            stars = string_to_array(row["stars"])
            date = row["date"].split(' ')[1]

            return {"numbers": numbers, "stars":  stars, "date": date}

        # apply a function on each row of the dataset
        series = self.__raw_data.apply(func, axis=1)

        return np.array(series)


business = Business()
