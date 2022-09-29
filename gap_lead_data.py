import pandas
from matplotlib import pyplot as plt
from typing import Dict, Tuple
import fastf1
import fastf1.plotting
import statistics
import json
import math

from copy import deepcopy

fastf1.plotting.setup_mpl()
RUN_SESSION = True


class GapLeadData:
    def __init__(self):
        # Set the cache
        fastf1.Cache.enable_cache('f1cache')
        self.session = fastf1.get_session(2019, 'Spanish', 'R')
        if RUN_SESSION:
            self.session.load()
        self.very_short_list_of_car_numbers = ["44", "77"]
        self.list_of_car_numbers = ['44', '77', '33', '5', '16', '10', '20', '55', '26', '8', '23', '3', '27', '7', '11', '99', '63', '88', '18', '4']




fastf1.Cache.enable_cache('f1cache')
session = fastf1.get_session(2019, 'Spanish', 'R')
if RUN_SESSION:
    session.load()
very_short_list_of_car_numbers = ["44", "77"]
list_of_car_numbers = ['44', '77', '33', '5', '16', '10', '20', '55', '26', '8', '23', '3', '27', '7', '11', '99', '63', '88', '18', '4']

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


def get_timing_data(is_sorted: bool = True, short: bool = False) -> pandas.DataFrame:
    """
    # https://theoehrly.github.io/Fast-F1/api.html#fastf1.api.timing_data

    :param is_sorted: Whether to sort the data by time.
    :param short: Whether to return a sliced version of the dataset (a fraction of it) or not
    :return:
        ~~(DataFrame, DataFrame): The first DataFrame is the lap data, the second's the stream_data (with gap times!)~~
        DataFrame: We will just return the streaming data actually to make things easier for now

    """
    if is_sorted:
        if short:
            print("Getting short sorted timing data")
            return fastf1.api.timing_data(session.api_path)[1].sort_values('Time')[1000:1040]
        else:
            print("Getting long sorted timing data")
            return fastf1.api.timing_data(session.api_path)[1].sort_values('Time')
    else:
        if short:
            print("Getting short unsorted timing data")
            return fastf1.api.timing_data(session.api_path)[1][1000:1040]
        else:
            print("Getting long unsorted timing data")
            return fastf1.api.timing_data(session.api_path)[1]


def iterate_over_timing_data(stream_data: pandas.DataFrame, file=None, using_list: bool=True) -> None:
    """
    This function will iterate over the timing data... getting tired, will come back to this tmrw.
    """
    stats = {}

    # Clean up this algorithm and write notes on it. Or at least upload the photo to Notion

    less_than_half: bool = True  # This variable keeps track of whether we have changed to the next half second or not.
    last_state: bool = less_than_half  # This just keeps track of the last value of less_than_half.

    dict_with_list = {"streaming_data" : []}

    count = 0

    for index, row in stream_data.iterrows():
        value = (row['Time'].total_seconds() * 10) % 10

        less_than_half = value < 5  # If True, we are in the first half of the second

        if less_than_half != last_state:
            # We have changed to the next half second.
            # Do logic here
            # TODO: add tests to ensure this is working. For everything really
            # print("We have changed to the next half second.")
            last_state = less_than_half
            if file is not None:
                if not using_list:
                    json.dump(stats, file, indent=4)
                    file.write("\n")
                else:
                    dict_with_list["streaming_data"].append(stats)
            stats = {}  # Reset the stats dictionary.

        # Fill in the stats dictionary
        # Just use the last timestep before the .5 and .0 mark for now, but come back to clean this up.
        # We want the timesteps to be in 0.5 intervals, and also to allow for cases where the gap between timestamps
        # is greater than 1 second.

        # Total seconds, rounded down.
        total_seconds = math.floor(row['Time'].total_seconds())
        if less_than_half is not True:
            total_seconds += 0.5

        # This could probably be done with a dictionary comprehension, but I'm not sure if it's worth it.
        # I could probably also make a function that does this to help tidy things up a bit.
        # This is just to handle reinitialization of the stats dictionary.
        stats["ts"] = total_seconds
        try:
            stats["car_number"][row['Driver']] = {}
            stats["car_number"][row['Driver']]["gap_to_leader"] = row['GapToLeader']
            stats["car_number"][row['Driver']]["gap_to_postiion_ahead"] = row['IntervalToPositionAhead']
            stats["car_number"][row['Driver']]["updated"] = "True"

        except:
            stats["car_number"] = {}
            stats["car_number"][row['Driver']] = {}
            stats["car_number"][row['Driver']]["gap_to_leader"] = row['GapToLeader']
            stats["car_number"][row['Driver']]["gap_to_postiion_ahead"] = row['IntervalToPositionAhead']
            stats["car_number"][row['Driver']]["updated"] = "True"

        for number in list_of_car_numbers:
            if number not in stats["car_number"]:
                stats["car_number"][str(number)] = {"gap_to_leader" : "999", "gap_to_position_ahead" : "999", "updated" : "False"}

        count+=1
        if count >= 600:
            break

    if using_list:
        json.dump(dict_with_list, file, indent=4)
    print(stats)


# Note: that I am coming back to this now later, and I have no idea what the 'new_timing' part of this function is.

# TODO: note that I am just copying the above function... this is messy as hell but I'm tired so will fix this up later
# Note: there might be some weird pointer/ memory stuff going on right now. Will need to use decopy. will sort this out tmrw
def iterate_over_timing_data_with_new_timing(stream_data: pandas.DataFrame, short: bool, file = None, using_list: bool = True) -> None:
    """
    This function will iterate over the timing data... getting tired, will come back to this tmrw.
    """
    stats = {}
    # For keeping track of udpated cars
    updated_cars = []


    # Clean up this algorithm and write notes on it. Or at least upload the photo to Notion

    less_than_half: bool = True  # This variable keeps track of whether we have changed to the next half second or not.
    last_state: bool = less_than_half  # This just keeps track of the last value of less_than_half.

    dict_with_list = {"streaming_data" : []}

    count = 0

    # Initialize the dict outside the main loop
    stats["car_number"] = {}
    if short:
        for number in very_short_list_of_car_numbers:
            if number not in stats["car_number"]:
                stats["car_number"][str(number)] = {"gap_to_leader" : "999", "gap_to_position_ahead" : "999", "updated" : "False"}
    else:
        for number in list_of_car_numbers:
            if number not in stats["car_number"]:
                stats["car_number"][str(number)] = {"gap_to_leader": "999", "gap_to_position_ahead": "999", "updated": "False"}

    for index, row in stream_data.iterrows():
        value = (row['Time'].total_seconds() * 10) % 10

        less_than_half = value < 5
        if less_than_half != last_state:
            # We have changed to the next half second.
            # Do logic here
            # TODO: add tests to ensure this is working. For everything really
            last_state = less_than_half
            if file is not None:

                # TODO: HARCODED SHORT LIST
                for number in very_short_list_of_car_numbers:
                    if number not in updated_cars:
                        stats["car_number"][str(number)]["u"] = "False"

                if not using_list:
                    json.dump(stats, file, indent=4)
                    file.write("\n")
                else:
                    dict_with_list["streaming_data"].append(deepcopy(stats))

            # Reinitialize the updated_cars list
            updated_cars = []

        total_seconds = math.floor(row['Time'].total_seconds())
        if not less_than_half:
            total_seconds += 0.5

        print("total seconds: ", total_seconds)

        # Just going to use a manual count here for setting the timestamp. I am going to need a plan for how to skip
        # when the original dataset doesn't have a matching timestamp.
        # TODO: I need to write this plan out. 28/9/22.
        #  it might even be a good idea for me to just copy this function down, and then rewrite it.
        # if count == 0:
        #     print("First time")
        #     manual_timestamp = total_seconds
        #     print(manual_timestamp)
        # else:
        #     manual_timestamp = manual_timestamp + 0.5

        # This could probably be done with a dictionary comprehension, but I'm not sure if it's worth it.
        # I could probably also make a function that does this to help tidy things up a bit.
        # This is just to handle reinitialization of the stats dictionary.

        stats["ts"] = total_seconds
        # stats["ts"] = manual_timestamp


        # TODO: HARDCODED list_of_car_numbers (I should be able to select between very short list, and normal list)
        try:
            if str(row['Driver']) in list_of_car_numbers:
                stats["car_number"][row['Driver']] = {}
                stats["car_number"][row['Driver']]["i1"] = row['GapToLeader']
                stats["car_number"][row['Driver']]["i2"] = row['IntervalToPositionAhead']
                stats["car_number"][row['Driver']]["u"] = "True"
                updated_cars.append(row['Driver'])
        except:
            stats["car_number"] = {}

        count+=1

        # TODO: check this out! This needs to be removed going forward... clean the f out of this codebase (politely)!
        # Note: this is what we were using for controlling the size of the dataset... not the `get_dataset` function.
        # 600 for very short dataset, and 3000 for short dataset... just comment out for full dataset.
        # Clean this up!!!
        # TODO: HARDCODED
        if count >= 300:
             break

    if using_list:
        json.dump(dict_with_list, file, indent=4)
    print(stats)





def print_car_data():
    print(session.car_data.keys())
    print(session.car_data["44"].columns)

    print(session.pos_data.keys())
    print(session.pos_data["44"].columns)


def write_to_json_file(filename: str, stream_data: pandas.DataFrame) -> None:
    """
    This function will write the data to a json file.
    :param filename:
    :return:
    """
    with open(filename, 'w+') as f:
        # iterate_over_timing_data(stream_data, f)
        # TODO: note there is an important variable here (`short`) that controls whether we are using the short list or
        #  not.
        #  This should be set outside of this function!
        iterate_over_timing_data_with_new_timing(stream_data, short=False, file=f)


def main():
    stream_data = get_timing_data(short=False)
    print_pandas_dataframe_info(stream_data)
    # iterate_over_timing_data(stream_data)
    write_to_json_file('test.json', stream_data)
    # print_car_data()


if __name__ == '__main__':
    main()
