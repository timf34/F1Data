from copy import deepcopy
import pandas
from typing import Dict, Tuple, List
import fastf1
import fastf1.plotting
import json

fastf1.plotting.setup_mpl()

RUN_SESSION = True


class MostRecentLapTime:
    def __init__(self):
        # Set the cache
        fastf1.Cache.enable_cache('f1cache')
        self.session = fastf1.get_session(2019, 'Spanish', 'R')
        if RUN_SESSION:
            self.session.load()

        self.laps = self.session.load_laps()

    def check_if_lap_data_is_equal(self, car_number: str) -> pandas.DataFrame:
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



def main():
    most_recent_lap_time = MostRecentLapTime()
    laps = most_recent_lap_time.laps




if __name__ == '__main__':
    main()
