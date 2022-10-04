import json
import math
from typing import List

# Note this file will be very hardcodey by nature

# This file was used to convert our current telemetry data to 4fps from 2FPS.
# It iterates through the lists of our dataset, and interpolates the data (including for the timestamps, bring it to
# 4fps -> 3.5, 4, 4.5 goes to 3.5, 3.75, 4, 4.25, 4.5)

# It is very messy code and I don't plan to clean it up as I really shouldn't need to use it again anytime soon.


# Note: I could put `convert_to_4fps` and `convert_data_to_list` into one file.

class ConvertTo4FPS:
    def __init__(self):
        self.path_to_data: str = "data/new_json_file_with_lap_times.json"
        self.path_to_output: str = "data/new_json_file_with_lap_times_4fps.json"
        self.data = self.load_json()
        # self.samp_data = {"streaming_data" : [[1, 2, "NaN", 3, "timestamp", 5], [3, 4, 69, 5, "timestamp", 5.5], [5, 6, "yolo", 7, "timestamp", 6]]}

    def load_json(self) -> dict:
        with open(self.path_to_data, "r") as f:
            data = json.load(f)
        return data

    def convert_to_4fps(self) -> dict:
        """
            I need to iterate through the current list, and the next one, and interpolate values between them (the
            current dataset is at 2FPS with a timestamp every 0.5 seconds). I will then move to the next list, and place
            the interpolated list in the index behind it.
        """
        new_data = []
        # 'i' is the int index, _list is the list
        for index, _list in enumerate(self.data["streaming_data"]):
            if index % 2 == 1:
                continue
            try:
                for v1, v2 in zip(_list, self.data["streaming_data"][index + 1]):
                    # Convert to an int if I can, otherwise leave it as a string
                    try:
                        v1 = float(v1)
                        v2 = float(v2)
                    except ValueError:
                        pass
                    # Interpolate values
                    if all([isinstance(v1, float), isinstance(v2, float)]):

                        # When I want to convert NaN's to "NaN"s I can use this..
                        # Except that this isn't a correct implemenation! Its working now anyways... just ctrl + r
                        # to change the NaN's to "NaN" in the json file if I want to.
                        # try:
                        #     if math.isnan(v1) or math.isnan(v2):
                        #         new_data.append("\"NaN\"")
                        # except ValueError:
                        #     new_data.append((v1 + v2) / 2)

                        if v1 == 999 and v2 != 999:
                            new_data.append(v2)
                        elif v2 == 999 and v1 != 999:
                            new_data.append(v1)
                        else:
                            interpolated_value = (v1 + v2) / 2
                            new_data.append(round(interpolated_value, 2))
                    else:
                        new_data.append(v1)
                self.data["streaming_data"].insert(index + 1, new_data)
                new_data = []
            except IndexError:
                print("Reached end of list - would raise IndexError")

        # Write self.data to a new json file
        with open(self.path_to_output, "w") as f:
            json.dump(self.data, f, indent=4)


def main():
    converter = ConvertTo4FPS()
    converter.convert_to_4fps()


if __name__ == "__main__":
    main()
