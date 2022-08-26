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
    print("dataframe sorted by Time: \n", dataframe.sort_values(by='Time')[3000:3040], "\n")


def get_timing_data(sorted: bool = True) -> pandas.DataFrame:
    """
    # https://theoehrly.github.io/Fast-F1/api.html#fastf1.api.timing_data
    :return:
        ~~(DataFrame, DataFrame): The first DataFrame is the lap data, the second's the stream_data (with gap times!)~~
        DataFrame: We will just return the streaming data actually to make things easier for now

    """
    if sorted:
        print("Getting sorted timing data")
        return fastf1.api.timing_data(session.api_path)[1].sort_values('Time')[1000:1040]
    else:
        print("Getting unsorted timing data")
        return fastf1.api.timing_data(session.api_path)[1]


def iterate_over_timing_data(stream_data: pandas.DataFrame, file = None) -> None:
    """
    This function will iterate over the timing data... getting tired, will come back to this tmrw.
    """
    stats = {}

    less_than_half: bool = True  # This variable keeps track of whether we have changed to the next half second or not.
    last_state: bool = less_than_half  # This just keeps track of the last value of less_than_half.

    for index, row in stream_data.iterrows():
        value = (row['Time'].total_seconds() * 10) % 10
        if value < 5:
            less_than_half = True  # We are in the first half second of the second.
        else:
            less_than_half = False

        if less_than_half != last_state:
            # We have changed to the next half second.
            # Do logic here
            print("We have changed to the next half second.")
            last_state = less_than_half
            if file is not None:
                json.dump(stats, file, indent=4)
            stats = {}  # Reset the stats dictionary.

        # Fill in the stats dictionary
        # Just use the last timestep before the .5 and .0 mark for now, but come back to clean this up.
        # We want the timesteps to be in 0.5 intervals, and also to allow for cases where the gap between timestamps
        # is greater than 1 second.
        stats["timestamp"] = row['Time'].total_seconds()
        stats["car_number"] = row['Driver']
        stats["gap_to_leader"] = row['GapToLeader']
        stats["gap_to_postiion_ahead"] = row['IntervalToPositionAhead']



        # print(row)
        # stats["timestamp"] = row['Time'].total_seconds()
        # print("Here is the row \n", row)
        # print("Here is the index\n", index)
        # count += 1
        # if int((row['Time'].total_seconds() * 10) % 10) <= 4:  # This would exclude all times between 0.5 and 0.999 rn
        #     # Note that by placing this here, we would still get the car that is the first one to be greater than 0.5
        #     # which is a bit of an issue. I am sure there is a smarter way to do this, but I will leave it like this for now
        #     # Note that I should also include the real timesteps in the dictionary to help with debugging.
        #     print(stats)
        #     stats = {}


    print(stats)


def write_to_json_file(filename: str, stream_data: pandas.DataFrame) -> None:
    """
    This function will write the data to a json file.
    :param filename:
    :return:
    """
    with open(filename, 'w') as f:
        iterate_over_timing_data(stream_data, f)



def main():
    stream_data = get_timing_data()
    # print_pandas_dataframe_info(stream_data)
    # iterate_over_timing_data(stream_data)
    write_to_json_file('stream_data.json', stream_data)


if __name__ == '__main__':
    main()
