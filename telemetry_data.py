import pandas
from copy import deepcopy
from matplotlib import pyplot as plt
from typing import Dict, Tuple
import fastf1
import fastf1.plotting
from collections import defaultdict
import statistics
import json
import math

from utils import load_json_file, parse_our_json_dict

fastf1.plotting.setup_mpl()

RUN_SESSION = True


class TelemetryData:
    def __init__(self):
        # Set the cache
        fastf1.Cache.enable_cache('f1cache')
        self.session = fastf1.get_session(2019, 'Spanish', 'R')
        if RUN_SESSION:
            self.session.load()

        self.list_of_car_numbers = ['44', '77', '33', '5', '16', '10', '20', '55', '26', '8', '23', '3', '27', '7', '11', '99', '63', '88', '18', '4']
        self.data = self.get_car_data()
    def print_pandas_dataframe_info(self):
        # Not sure if this is actually very descriptive, but it will do for now.
        print("dataframe columns: \n", self.data["44"].columns, "\n")
        print("dataframe shape: \n",self.data["44"].shape, "\n")
        print("dataframe info: ",self.data["44"].info(), "\n")
        print("dataframe head: \n", self.data["44"].head(), "\n")
        print("dataframe tail: \n",self.data["44"].tail(), "\n")
        print("dataframe attributes: \n", self.data["44"].__dict__.keys(), "\n")

        print(
            "We will now print the some random values 1000 rows into the dataframe object, after it has been sorted by"
            "Time")
        print("dataframe sorted by Time: \n", self.data["44"].sort_values(by='Time')[3000:3040], "\n")

    def random_row_practice(self):
        print("time of 9000th row: ", self.data["44"].iloc[9000]["Time"], type(self.data["44"].iloc[9000]["Time"]))
        print("session time of 9000th row: ", self.data["44"].iloc[9000]["SessionTime"], type(self.data["44"].iloc[9000]["SessionTime"]))
        print("total seconds of 7500th row: ", self.data["44"].iloc[7500]["SessionTime"].total_seconds(), type(self.data["44"].iloc[9000]["SessionTime"].total_seconds()))
        print("total seconds of 9000th row: ", self.data["44"].iloc[9000]["SessionTime"].total_seconds(), type(self.data["44"].iloc[9000]["SessionTime"].total_seconds()))

    def get_car_data(self) -> Dict[str, pandas.DataFrame]:
        """
        This function will return a dictionary with the car data for each car in the list_of_car_numbers list.

        :return: A dictionary with the car data for each car in the list_of_car_numbers list.
                 i.e. {'44': car_data_44, '77': car_data_77, ...}
        """
        return self.session.car_data

    def create_list_with_dicts(self, short_list: bool = True) -> list:

        big_list = []

        # initialize dict structure
        temp_dict = {}
        temp_dict["car_number"] = {}
        for car_number in self.list_of_car_numbers:
            temp_dict["car_number"][car_number] = {"speed": "", "throttle": "", "brake": "", "rpm": "", "gear": ""}

        print(temp_dict)

        # create a list of dataframes for the telemetry data for each car
        # Note: we are appendinng dataframes.iterrows() to the list, not the dataframes themselves.
        dataframes = []
        for car_number in self.list_of_car_numbers:
            if short_list:
                _dataframe = self.data[car_number][7000:8500]
            else:
                _dataframe = self.data[car_number]
            dataframes.append((car_number, _dataframe.iterrows()))

        length = len(_dataframe)
        print("length of a dataframe: ", length)

        # iterate through the dataframes and create a list of dicts with the data
        for i in range(length):
            for car_number, iterrows in dataframes:
                info = next(iterrows)
                temp_dict["timestamp"] = info[1]["Time"].total_seconds()
                temp_dict["car_number"][car_number]["speed"] = info[1]["Speed"]
                temp_dict["car_number"][car_number]["throttle"] = info[1]["Throttle"]
                temp_dict["car_number"][car_number]["brake"] = info[1]["Brake"]
                temp_dict["car_number"][car_number]["gear"] = info[1]["nGear"]
                temp_dict["car_number"][car_number]["rpm"] = info[1]["RPM"]
            big_list.append(deepcopy(temp_dict))

        return big_list


def merging_telemetry_with_timing_data():
    timing_data = load_json_file("stream_data.json")

    # for i in timing_data["streaming_data"]:
    #      print(i)

    # sample_timstampes = [1955, 2000, 2050]

    telemetry_data = TelemetryData()
    telemetry_list = telemetry_data.create_list_with_dicts(short_list=False)

    # I should make a function for this creation of a dict with car_numbers, etc. I repeat it a lot.
    temp_dict = {"car_number": {}}
    for car_number in telemetry_data.list_of_car_numbers:
        temp_dict["car_number"][car_number] = {}

    another_big_list = []

    for i in timing_data["streaming_data"]:
        for j in telemetry_list:
            if j["timestamp"] >= float(i["timestamp"]):
                for car_number in telemetry_data.list_of_car_numbers:
                    # The pointers/ expression here merges two dicts:)
                    i["car_number"][car_number] =  {**j["car_number"][car_number], **i["car_number"][car_number]}
                    temp_dict["car_number"][car_number] = {**j["car_number"][car_number], **i["car_number"][car_number]}
                    temp_dict["timestamp"] = i["timestamp"]

                # print(f"temp dict: {temp_dict}")
                another_big_list.append(deepcopy(temp_dict))
                break

    # print("another big list: ", another_big_list)
    # print("length of another big list: ", len(another_big_list))

    new_dict = {"streaming_data": another_big_list}

    # Write this new dict to a file
    with open("stream_data.json", "w") as f:
        json.dump(new_dict, f, indent=4)
        f.write("\n")


def main():
    telemetry_data = TelemetryData()
    # telemetry_data.print_pandas_dataframe_info()
    # telemetry_data.random_row_practice()
    # telemetry_data.create_list_with_dicts()
    merging_telemetry_with_timing_data()


if __name__ == '__main__':
    main()