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
        self.timing_data = self.lets_get_timing_data(is_sorted=True, short=False)

    def lets_get_timing_data(self, is_sorted: bool = True, short: bool = False) -> pandas.DataFrame:
        """
            This function takes a dataframe as an argument, then prints useful information about said dataFrame
            (i.e. columns, number of rows, etc.)
            :param dataframe:
            :return:
        """
        if is_sorted:
            if short:
                print("Getting short sorted timing data")
                return fastf1.api.timing_data(self.session.api_path)[1].sort_values('Time')[1000:1040]
            else:
                print("Getting long sorted timing data")
                return fastf1.api.timing_data(self.session.api_path)[1].sort_values('Time')
        else:
            if short:
                print("Getting short unsorted timing data")
                return fastf1.api.timing_data(self.session.api_path)[1][1000:1040]
            else:
                print("Getting long unsorted timing data")
                return fastf1.api.timing_data(self.session.api_path)[1]


    def iterate_over_timing_data(self, stream_data: pandas.DataFrame, short: bool, file = None, using_list: bool = True):
        """
            This function will iterate over the timing data... getting tired, will come back to this tmrw.
        """
        # For keeping track of udpated cars
        updated_cars = []

        less_than_half: bool = True  # This variable keeps track of whether we have changed to the next half second/ not
        last_state: bool = less_than_half  # This just keeps track of the last value of less_than_half.

        dict_with_list = {"streaming_data": []}
        count = 0

        stats = {"car_number": {}}
        if short:
            for number in self.very_short_list_of_car_numbers:
                if number not in stats["car_number"]:
                    stats["car_number"][str(number)] = {"gap_to_leader": "999",
                                                        "gap_to_position_ahead": "999",
                                                        "updated": "False"}
        else:
            for number in self.list_of_car_numbers:
                if number not in stats["car_number"]:
                    stats["car_number"][str(number)] = {"gap_to_leader": "999",
                                                        "gap_to_position_ahead": "999",
                                                        "updated": "False"}

        for index, row in stream_data.iterrows():
            decimal_second = (row['Time'].total_seconds() * 10) % 10

            less_than_half = decimal_second < 5
            if less_than_half != last_state:
                last_state = less_than_half
                if file is not None:
                    if short:
                        for number in self.very_short_list_of_car_numbers:
                            if number not in updated_cars:
                                stats["car_number"][str(number)]["u"] = "False"
                    else:
                        for number in self.list_of_car_numbers:
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

            stats["ts"] = total_seconds

            try:
                if short:
                    list_we_are_using = self.very_short_list_of_car_numbers
                else:
                    list_we_are_using = self.list_of_car_numbers
                if str(row['Driver']) in list_we_are_using:
                    stats["car_number"][row['Driver']] = {}
                    stats["car_number"][row['Driver']]["i1"] = row['GapToLeader']
                    stats["car_number"][row['Driver']]["i2"] = row['IntervalToPositionAhead']
                    stats["car_number"][row['Driver']]["u"] = "True"
                    updated_cars.append(row['Driver'])
            except:
                stats["car_number"] = {}

            count += 1

            # TODO: check this out! This needs to be removed going forward... clean the f out of this codebase (politely)!
            #  HARDCODED
            if short:
                if count >= 200:
                    break

        if using_list:
            json.dump(dict_with_list, file, indent=4)

    def write_to_json_file(self, filename: str, stream_data: pandas.DataFrame) -> None:
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
            self.iterate_over_timing_data(stream_data, short=True, file=f)


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


def main():
    # stream_data = get_timing_data(short=True)
    # print_pandas_dataframe_info(stream_data)
    # write_to_json_file('test.json', stream_data)
    # print_car_data()

    timing_data = GapLeadData()
    streaming_data = timing_data.lets_get_timing_data(short=True)
    timing_data.write_to_json_file('class_test.json', streaming_data)


if __name__ == '__main__':
    main()
