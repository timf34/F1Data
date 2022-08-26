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
fastf1.Cache.enable_cache('../f1cache')
session = fastf1.get_session(2019, 'Spanish', 'R')
if RUN_SESSION:
    session.load()


def print_session_results():
    print("sessions results")
    print(session.results)
    print(session.results.columns)


def print_session_laps():
    print("sesion laps")
    print(session.laps)
    print(session.laps.columns)
    print("\nsession attributes")
    # print(session.__dict__.keys())


def print_car_data():
    print("car data")
    print(session.car_data)
    print(session.car_data.keys())
    print(session.car_data['44'].columns)


def print_pos_data():
    print("pos data")
    print(session.pos_data)
    print(session.pos_data.keys())
    print(session.pos_data['44'].columns)


def create_empty_dict_structure() -> Dict:
    sample_dict = {}
    # sample_dict["rankings"] = {}
    sample_dict["car_data"] = {}
    sample_dict["car_data"]["44"] = {}

    return sample_dict


def get_car_pos_data() -> Dict:
    return session.pos_data


def convert_car_pos_data_dict() -> Dict:
    pos_data = get_car_pos_data()

    sample_dict = create_empty_dict_structure()

    sample_dict["timestamp"] = pos_data["44"].loc[0, 'Date']

    sample_dict["car_data"]["44"] = {}
    sample_dict["car_data"]["44"]["x_pos"] = pos_data["44"].loc[0, 'X']
    sample_dict["car_data"]["44"]["y_pos"] = pos_data["44"].loc[0, 'Y']
    sample_dict["car_data"]["44"]["z_pos"] = pos_data["44"].loc[0, 'Z']

    print(sample_dict)
    return sample_dict


def using_iterrows() -> None:
    pos_data = get_car_pos_data()

    sample_dict = create_empty_dict_structure()

    for index, row in pos_data["44"].iterrows():
        sample_dict["car_data"]["44"]["x_pos"] = row["X"]
        sample_dict["car_data"]["44"]["y_pos"] = row["Y"]
        sample_dict["car_data"]["44"]["z_pos"] = row["Z"]
        sample_dict["timestamp"] = row["Date"]
        print(sample_dict)


def using_next_simple() -> None:
    pos_data = get_car_pos_data()
    print(next(pos_data["44"].iterrows()))
    print("done here now")


def using_next_for_all_cars() -> None:
    pos_data = get_car_pos_data()
    car_numbers = []
    for key in pos_data:
        car_numbers.append(key)
    print(car_numbers)
    sample_dict = create_empty_dict_structure()

    for i in car_numbers:
        sample_dict["car_data"][i] = {}


    # I want to use next() over all the cars... one at a time too. That means I need to instatiate all the dataframes.
    # I could actually just instatiate a list of the dataframes, and then iterate through those. Or a list of tuples
    # Would work too. Where the first index is the car number.

    # I can't remember completely, but I think there might have been a dataframe for each car here?

    dataframes = []
    for car_number in car_numbers:
        dataframes.append((car_number, pos_data[car_number].iterrows()))


    length = len(pos_data['44'])
    print("legnth", length)

    print(dataframes)
    big_list = []
    x_pos = []
    y_pos = []
    z_pos = []

    # I should have drawn out how this algorithm flows and uploaded it to Notion.

    for i in range(length):
        for car_number, iterrows in dataframes:
            info = next(iterrows)
            # print(car_number)
            # print(info)
            # print(car_number, info)
            sample_dict["timestamp"] = str(info[1]["Time"])
            sample_dict["car_data"][car_number]["x_pos"] = info[1]["X"]
            x_pos.append(info[1]["X"])
            sample_dict["car_data"][car_number]["y_pos"] = info[1]["Y"]
            y_pos.append(info[1]["Y"])
            sample_dict["car_data"][car_number]["z_pos"] = info[1]["Z"]
            z_pos.append(info[1]["Z"])
        big_list.append(sample_dict.copy())

    # print(big_list)
    # print(len(big_list))

    # Find the max of the list of x_pos
    max_x = max(x_pos)
    max_y = max(y_pos)
    max_z = max(z_pos)
    print("max x", max_x)
    print("max y", max_y)
    print("max z", max_z)

    # Find the min of the list of x_pos
    min_x = min(x_pos)
    min_y = min(y_pos)
    min_z = min(z_pos)
    print("min x", min_x)
    print("min y", min_y)
    print("min z", min_z)

    # Find the mean of the list of x_pos
    mean_x = sum(x_pos) / len(x_pos)
    mean_y = sum(y_pos) / len(y_pos)
    mean_z = sum(z_pos) / len(z_pos)
    print("mean x", mean_x)
    print("mean y", mean_y)
    print("mean z", mean_z)

    # Find the median of the list of x_pos
    median_x = statistics.median(x_pos)
    median_y = statistics.median(y_pos)
    median_z = statistics.median(z_pos)
    print("median x", median_x)
    print("median y", median_y)
    print("median z", median_z)

    # Find the mode of the list of x_pos
    mode_x = statistics.mode(x_pos)
    mode_y = statistics.mode(y_pos)
    mode_z = statistics.mode(z_pos)
    print("mode x", mode_x)
    print("mode y", mode_y)
    print("mode z", mode_z)

    # Find the variance of the list of x_pos
    variance_x = statistics.variance(x_pos)
    variance_y = statistics.variance(y_pos)
    variance_z = statistics.variance(z_pos)
    print("variance x", variance_x)
    print("variance y", variance_y)
    print("variance z", variance_z)

    # Find the standard deviation of the list of x_pos
    standard_deviation_x = statistics.stdev(x_pos)
    standard_deviation_y = statistics.stdev(y_pos)
    standard_deviation_z = statistics.stdev(z_pos)
    print("standard deviation x", standard_deviation_x)
    print("standard deviation y", standard_deviation_y)
    print("standard deviation z", standard_deviation_z)

    # Find the range of the list of x_pos
    range_x = max_x - min_x
    range_y = max_y - min_y
    range_z = max_z - min_z
    print("range x", range_x)
    print("range y", range_y)
    print("range z", range_z)

    # Find the midrange of the list of x_pos
    midrange_x = (max_x + min_x) / 2
    midrange_y = (max_y + min_y) / 2
    midrange_z = (max_z + min_z) / 2
    print("midrange x", midrange_x)
    print("midrange y", midrange_y)
    print("midrange z", midrange_z)

    return big_list


def create_file_with_jsons() -> None:
    # This function will append (via pretty print) json objects to a file.
    # The file will be named "data.json"

    # Get list of json objects
    json_list = using_next_for_all_cars()
    # print(json_list)

    # Create file
    with open("../data.json", "w") as outfile:
        for json_object in json_list:
            json.dump(json_object, outfile, indent=4)
            outfile.write("\n")


def calculate_distance_between_two_cars(car1: Tuple[int, int, int], car2: Tuple[int, int, int]) -> float:
    # This function will calculate the distance between two cars.
    # The input is a tuple of the x, y, and z positions of the cars.
    # Note that the x, y, z positions are cartesian coordinates and can be negative or positive
    # The output is to be normalized between 0 and 1.

    # Dive the input by 3 to get the units in metres (its currently 1/3 of a metre)
    car1 = tuple(x / 3 for x in car1)
    car2 = tuple(x / 3 for x in car2)

    max_distance = abs


    # Calculate the distance between the two cars
    # We will just use x and y to simplify things
    distance = math.sqrt((car1[0] - car2[0]) ** 2 + (car1[1] - car2[1]) ** 2)
    print("distance", distance)

    # Normalize the distance between 0 and 1
    normalized_distance = distance / 5265.65 #  Just got by getting the max and min values.
    print("normalized distance", normalized_distance)

    normalized_distance *= 70

    return normalized_distance







def trying_calculate_distance_between_two_cars() -> None:

    # Sample inputs
    a1 = (1238, 3322, 1820)
    a2 = (-8796, -8875, 1744)

    calculate_distance_between_two_cars(a1, a2)


def get_timing_data():
    print("Printing session attributes")
    print(session.__dict__)

    laps_data, stream_data = fastf1.api.timing_data(session.api_path)
    print("Printing laps data")
    print(laps_data)

    print("Printing stream data")
    print(stream_data)



if __name__ == '__main__':
    # convert_car_pos_data_dict()
    # using_iterrows()
    # using_next_simple()
    # using_next_for_all_cars()
    # create_file_with_jsons()
    # trying_calculate_distance_between_two_cars()
    get_timing_data()

