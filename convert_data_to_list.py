import json

from typing import Dict, List

from utils import load_json_file

# Note: I could put `convert_to_4fps` and `convert_data_to_list` into one file.


class ConvertDataToList:
    def __init__(self):
        self.data_file: str = "data/stream_data_with_lap_times.json"
        self.new_file_name: str = "data/new_json_file_with_lap_times.json"
        self.indent: int = 2

    def print_info(self):
        data = load_json_file(self.data_file)
        print("Data type: ", type(data))
        print("Data keys: ", data.keys())
        print("Data values: ", data.values())
        print("Data: ", data)

    def convert_data_to_list(self) -> List[List]:
        data = load_json_file(self.data_file)

        big_list = []
        temp_list = []

        for i in data["streaming_data"]:
            for j in i["car_number"]:
                temp_list.extend((j,
                                  i["car_number"][j]["s"],
                                  i["car_number"][j]["t"],
                                  i["car_number"][j]["b"],
                                  i["car_number"][j]["r"],
                                  i["car_number"][j]["g"],
                                  i["car_number"][j]["i1"],
                                  i["car_number"][j]["i2"],
                                  i["car_number"][j]["u"],
                                  i["car_number"][j]["mostRecentLapTime"],
                                  "\n"
                                  ))
                # Note: using list.extend so as not to create a nested structure.
                # temp_list.extend((j,
                #                   i["car_number"][j]["speed"],
                #                   i["car_number"][j]["throttle"],
                #                   str(i["car_number"][j]["brake"]),
                #                   i["car_number"][j]["rpm"],
                #                   i["car_number"][j]["gear"],
                #                   str(i["car_number"][j]["gap_to_leader"]),
                #                   str(i["car_number"][j]["gap_to_postiion_ahead"]),
                #                   i["car_number"][j]["updated"],
                #                   "\n"
                #                   ))

            temp_list.append("timestamp")
            # temp_list.append(i["timestamp"])  # Append the timestamp to the end of the list.
            temp_list.append(i["ts"])  # Append the timestamp to the end of the list.
            big_list.append(temp_list)
            temp_list = []  # I should write down what this does, I think it resets the temp_list.

        return big_list

    def make_new_json_file(self):
        big_list = self.convert_data_to_list()
        our_dict = {}
        our_dict["streaming_data"] = big_list
        new_json_file = self.new_file_name
        with open(new_json_file, "w") as f:
            json.dump(our_dict, f, indent=self.indent)

    # This is a sort of 'working things out' function
    def lets_work_with_a_small_sample_dict(self):
        samp = {"streaming_data":
            [
                {
                    "car_number": {
                        "44": {
                            "s" : 200,
                            "r" : 1000
                        },
                        "77": {
                            "s": 228,
                            "r": 10747,
                        }
                    },
                    "ts": 1993
                },
                {
                    "car_number": {
                        "44": {
                            "s": 69,
                            "r": 1000
                        },
                        "77": {
                            "s": 420,
                            "r": "yolo",
                        }
                    },
                    "ts": 1993.5
                },

            ]
            }

        big_list = []
        temp_list = []

        for i in samp["streaming_data"]:
            for j in i["car_number"]:
                print(j, i["car_number"][j]["s"], i["car_number"][j]["r"], i["ts"])
                temp_list.append((j, i["car_number"][j]["s"], i["car_number"][j]["r"], i["ts"]))
            big_list.append(temp_list)
            temp_list = []

        print("big list: ", big_list)

    @staticmethod
    def working_with_lists(self):
        """
         Just want to test, appending things to a list without creating a nested list
        """
        list = []
        for i in range(10):
            list.append(i)
        print(list)

        list = []
        for i in range(10):
            list.append((i, i+1))
        print(list)

        list = []
        for i in range(10):
            list.extend((i, i+1))
        print(list)


if __name__ == '__main__':
    converter = ConvertDataToList()
    # converter.print_info()
    converter.make_new_json_file()
    # converter.working_with_lists()
