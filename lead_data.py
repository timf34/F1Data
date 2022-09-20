import pandas
from matplotlib import pyplot as plt
from typing import Dict, Tuple
import fastf1
import fastf1.plotting
import statistics
import json
import math

fastf1.plotting.setup_mpl()

RUN_SESSION = True

# Note: I started building this out as a class... which I should have done from the start... but it would take a bit
# longer to do this so I am going to go back to what I was already doing

list_of_car_numbers = ['44', '77', '33', '5', '16', '10', '20', '55', '26', '8', '23', '3', '27', '7', '11', '99',
                            '63', '88', '18', '4']

# TODO: note that I stopped refactoring this file into a class half way through doing so. This really needs to be
#  to be cleaned up. Read through it once fully and then refactor it into a class.

class LeadData:
    def __init__(self):
        # Set the cache
        fastf1.Cache.enable_cache('f1cache')
        self.session = fastf1.get_session(2019, 'Spanish', 'R')
        if RUN_SESSION:
            self.session.load()

        self.list_of_car_numbers = ['44', '77', '33', '5', '16', '10', '20', '55', '26', '8', '23', '3', '27', '7', '11', '99', '63', '88', '18', '4']

    def print_pandas_dataframe_info(self):
        print("dataframe columns: \n", self.data.columns, "\n")
        print("dataframe shape: \n",self.data.shape, "\n")
        print("dataframe info: ",self.data.info(), "\n")
        print("dataframe head: \n", self.data.head(), "\n")
        print("dataframe tail: \n",self.data.tail(), "\n")
        print("dataframe attributes: \n", self.data.__dict__.keys(), "\n")

        print(
            "We will now print the some random values 1000 rows into the dataframe object, after it has been sorted by"
            "Time")
        print("dataframe sorted by Time: \n", self.data.sort_values(by='Time')[3000:3040], "\n")

    @staticmethod
    def get_timing_data(self, short: bool):
        if sorted:
            if short:
                print("Getting short sorted timing data")
                self.data = fastf1.api.timing_data(self.session.api_path)[1].sort_values('Time')[1000:1040]
            else:
                print("Getting long sorted timing data")
                self.data = fastf1.api.timing_data(self.session.api_path)[1].sort_values('Time')
        else:
            if short:
                print("Getting short unsorted timing data")
                self.data = fastf1.api.timing_data(self.session.api_path)[1][1000:1040]
            else:
                print("Getting long unsorted timing data")
                self.data = fastf1.api.timing_data(self.session.api_path)[1]

    def print_car_data(self):
        print(self.session.car_data.keys())
        print(self.session.car_data["44"].columns)

        with open("car_data.txt", "w") as f:
            for i in self.session.car_data:
                print(i, self.session.car_data[i][10000:10100])
                f.write(str(self.session.car_data[i][10000:10100]))


        # print(self.session.pos_data.keys())
        # print(self.session.pos_data["44"].columns)





def iterate_over_timing_data(stream_data: pandas.DataFrame, file = None, using_list: bool = True) -> None:
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
        if value < 5:
            less_than_half = True  # We are in the first half second of the second.
        else:
            less_than_half = False

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
        stats["timestamp"] = total_seconds
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


# TODO: note that I am just copying the above function... this is messy as hell but I'm tired so will fix this up later
# Note: there might be some weird pointer/ memory stuff going on right now. Will need to use decopy. will sort this out tmrw
def iterate_over_timing_data_with_new_timing(stream_data: pandas.DataFrame, file = None, using_list: bool = True) -> None:
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
    for number in list_of_car_numbers:
        if number not in stats["car_number"]:
            stats["car_number"][str(number)] = {"gap_to_leader": "0", "gap_to_position_ahead": "0", "updated": "False"}

    for index, row in stream_data.iterrows():
        value = (row['Time'].total_seconds() * 10) % 10
        if value < 5:
            less_than_half = True  # We are in the first half second of the second.
        else:
            less_than_half = False

        if less_than_half != last_state:
            # We have changed to the next half second.
            # Do logic here
            # TODO: add tests to ensure this is working. For everything really
            # print("We have changed to the next half second.")
            last_state = less_than_half
            if file is not None:

                for number in list_of_car_numbers:
                    if number not in updated_cars:
                        stats["car_number"][str(number)]["updated"] = "False"

                if not using_list:
                    json.dump(stats, file, indent=4)
                    file.write("\n")
                else:
                    dict_with_list["streaming_data"].append(stats.copy())
            updated_cars = []
             # stats = {}  # Reset the stats dictionary.

        # Fill in the stats dictionary
        # Just use the last timestep before the .5 and .0 mark for now, but come back to clean this up.
        # We want the timesteps to be in 0.5 intervals, and also to allow for cases where the gap between timestamps
        # is greater than 1 second.

        # Total seconds, rounded down.
        # print("row['Time'] = ", row['Time'], "and row['Time'].total_seconds() = ", row['Time'].total_seconds())
        total_seconds = math.floor(row['Time'].total_seconds())
        if less_than_half is not True:
            total_seconds += 0.5

        # This could probably be done with a dictionary comprehension, but I'm not sure if it's worth it.
        # I could probably also make a function that does this to help tidy things up a bit.
        # This is just to handle reinitialization of the stats dictionary.
        stats["timestamp"] = total_seconds
        try:
            stats["car_number"][row['Driver']] = {}
            stats["car_number"][row['Driver']]["gap_to_leader"] = row['GapToLeader']
            stats["car_number"][row['Driver']]["gap_to_postiion_ahead"] = row['IntervalToPositionAhead']
            stats["car_number"][row['Driver']]["updated"] = "True"
            updated_cars.append(row['Driver'])
        except:
            pass

        # except:
        #     stats["car_number"] = {}
        #     stats["car_number"][row['Driver']] = {}
        #     stats["car_number"][row['Driver']]["gap_to_leader"] = row['GapToLeader']
        #     stats["car_number"][row['Driver']]["gap_to_postiion_ahead"] = row['IntervalToPositionAhead']
        #     stats["car_number"][row['Driver']]["updated"] = "True"

        # for number in list_of_car_numbers:
        #     if number not in stats["car_number"]:
        #         stats["car_number"][str(number)] = {"gap_to_leader" : "0", "gap_to_position_ahead" : "0", "updated" : "False"}

        count+=1
        if count >= 600:
            break

    if using_list:
        json.dump(dict_with_list, file, indent=4)
    print(stats)



def find_mean_timing_frequency(stream_data: pandas.DataFrame) -> Tuple[float, float]:
    """
    This function will find the frequency with which the timestamps are taken for an individual car.
    i.e. we'll find the average time between updates

    I will come back to this again, I'll need to subtract the timesteps. For now I'll just eyeball the data.
    :param stream_data:
    :return:
    """
    pass


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
        iterate_over_timing_data_with_new_timing(stream_data, f)


def main():
    # stream_data = get_timing_data()
    # print_pandas_dataframe_info(stream_data)
    # # iterate_over_timing_data(stream_data)
    # write_to_json_file('test_short_stream_data.json', stream_data)
    # # print_car_data()
    lead_data = LeadData()
    lead_data.print_car_data()


if __name__ == '__main__':
    main()
