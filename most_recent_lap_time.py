from copy import deepcopy
import pandas
from typing import Dict, Tuple, List, Union
import fastf1
import fastf1.plotting
import json
import math

from utils import load_json_file

fastf1.plotting.setup_mpl()

RUN_SESSION = True


class MostRecentLapTime:
    def __init__(self):
        # Set the cache
        fastf1.Cache.enable_cache('f1cache')
        self.session = fastf1.get_session(2019, 'Spanish', 'R')
        if RUN_SESSION:
            self.session.load()

        self.list_of_car_numbers = ['44', '77', '33', '5', '16', '10', '20', '55', '26', '8',
                                    '23', '3', '27', '7', '11', '99', '63', '88', '18', '4']
        # Lap data
        self.laps = self.session.load_laps()
        self.lap_data_per_car: Dict[str, pandas.DataFrame] = self.create_dict_with_pandas_dataframes()

        self.short_json_file: str = "data/stream_data_short_keys.json"


    def check_if_lap_data_is_equal(self, car_number: str) -> None:
        """
            This function takes a car number as an argument, then returns the data for that car.
            :param
                car_number: str
                    This is a string that represents the car number.
            :return:
                car_data: pandas.DataFrame
                    This is a pandas dataframe that contains the data for the car.
        """
        # print methods for self.session
        print(dir(self.session))
        print("Are these equal? ", pandas.DataFrame.equals(self.session.laps, self.session.load_laps()))

    @staticmethod
    def iterable_through_json_file(file_path: str) -> Dict[str, Dict[str, Dict[str, Union[int, str]]]]:
        """
            This function takes a file path as an argument, then iterates through the file.
            :param
                file_path: str
                    This is a string that represents the file path.
            :return:
        """
        # This function could be an iterator -> yield

        with open(file_path) as file:
            data = json.load(file)
            for count, i in enumerate(data["streaming_data"]):
                yield i

    def create_dict_with_pandas_dataframes(self) -> Dict[str, pandas.DataFrame]:
        # Note: this only returns an iterator!
        return {i: self.laps.pick_driver(i).iterrows() for i in self.list_of_car_numbers}

    def iterate_through_json_file(self) -> List:

        # Initialize the first lap time for each car (i.e. get the first row)
        lap_data = {i: next(self.lap_data_per_car[i]) for i in self.list_of_car_numbers}

        temp_dict = {"ts": 0, "car_number": {}}

        big_list = []

        # This iterates through the og dataset over each dict containing ("ts" and "car_number") keys
        for i in self.iterable_through_json_file(self.short_json_file):
            car_timestamp = i["ts"]
            temp_dict["ts"] = car_timestamp
            print("timestamp: ", car_timestamp)

            for car_num in self.list_of_car_numbers:

                lap_timestamp = lap_data[car_num][1].Time.total_seconds()
                print("lap timestamp: ", lap_timestamp)
                i["car_number"][car_num]["mostRecentLapTime"] = lap_data[car_num][1]["LapTime"].total_seconds()
                print("here is i car number: ", i["car_number"][car_num])

                if lap_timestamp <= car_timestamp:
                    print("yes it is less than")
                    try:
                        lap_data[car_num] = next(self.lap_data_per_car[car_num])
                    except StopIteration:
                        print("StopIteration - we are done with this car")
                        pass
                # Update our dict
                most_recent_time = lap_data[car_num][1]["LapTime"].total_seconds()
                if math.isnan(most_recent_time):
                    most_recent_time = 999
                i["car_number"][car_num]["mostRecentLapTime"] = most_recent_time
                temp_dict["car_number"][car_num] = i["car_number"][car_num]

            big_list.append(deepcopy(temp_dict))
        return big_list

    @staticmethod
    def make_our_json_file(dict_arg: List) -> None:
        """
            This function takes a List as an argument which makes up our {"streaming_data: []"} key.

            We then create a json file.
        """

        car_data = {"streaming_data": dict_arg}
        with open("data/stream_data_with_lap_times.json", "w") as file:
            json.dump(car_data, file, indent=2)


def main():
    most_recent_lap_time = MostRecentLapTime()
    big_list = most_recent_lap_time.iterate_through_json_file()
    most_recent_lap_time.make_our_json_file(big_list)



if __name__ == '__main__':
    main()
