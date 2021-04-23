import pandas as pd
import numpy as np


def prepare_arrays(series: pd.Series) -> np.array:
    """
        return a 2-darray out of pd.Series object
    """

    series = series.map(string_to_array)

    # transform the array of array into a 2d-array
    return np.stack(np.array(series.array))


def string_to_array(arg):
    """
        transform a stringified array ['1', '2']
        into a real array
    """

    res = arg.replace('[', '').replace(']', '').replace(',', '')
    return np.array(res.split(' '), dtype=np.int8)
