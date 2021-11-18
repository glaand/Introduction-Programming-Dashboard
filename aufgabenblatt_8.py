'''
Author: Alex
Date: 18. 11. 2021
Programming lanugage: Python 3.8.8
'''

# imports
import pandas as pd
import os

# Constants
DATA_PATH = os.path.join("datasets", "data.csv")


def load_data(path=None):
    if path is None:
        path = DATA_PATH
    with open(path) as file:
        return pd.read_csv(file)


if __name__ == "__main__":
    df = load_data()
