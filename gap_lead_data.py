import pandas
from matplotlib import pyplot as plt
from typing import Dict, Tuple
import fastf1
import fastf1.plotting
import statistics
import json
import math

fastf1.plotting.setup_mpl()

RUN_SESSION = False

# Set the cache
fastf1.Cache.enable_cache('f1cache')
session = fastf1.get_session(2019, 'Spanish', 'R')
if RUN_SESSION:
    session.load()


def print_pandas_dataframe_info(dataframe: pandas.DataFrame) -> None:
    """
    This function takes a dataframe as an argument, then prints useful information about said dataFrame
    (i.e. columns, number of rows, etc.)
    :param dataframe:
    :return:
    """
    print("dataframe columns: \n", dataframe.columns, "\n")
    print("dataframe shape: \n", dataframe.shape, "\n")
    print("dataframe info: ", dataframe.info(), "\n")
    print("dataframe head: \n", dataframe.head(), "\n")
    print("dataframe tail: \n", dataframe.tail(), "\n")
    print("dataframe attributes: \n", dataframe.__dict__.keys(), "\n")

    print("We will now print the some random values 1000 rows into the dataframe object, after it has been sorted by"
          "Time")
    print("dataframe sorted by Time: \n", dataframe.sort_values(by='Time')[1000:1040], "\n")


def get_timing_data() -> Tuple[pandas.DataFrame, pandas.DataFrame]:
    """
    # https://theoehrly.github.io/Fast-F1/api.html#fastf1.api.timing_data
    :return:
        (DataFrame, DataFrame): The first DataFrame is the lap data, the second is the stream_data (with gap times!)

    """
    return fastf1.api.timing_data(session.api_path)


def main():
    lap_data, stream_data = get_timing_data()
    print_pandas_dataframe_info(stream_data)


if __name__ == '__main__':
    main()
