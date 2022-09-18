import json

from typing import Dict, List

from utils import load_json_file


class ConvertDataToList:
    def __init__(self):
        self.data_file: str = "data/stream_data.json"
        self.new_file_name: str = "data/new_json_file.json"
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
                # temp_list.append((j,
                #                   i["car_number"][j]["s"],
                #                   i["car_number"][j]["t"],
                #                   i["car_number"][j]["b"],
                #                   i["car_number"][j]["r"],
                #                   i["car_number"][j]["g"],
                #                   i["car_number"][j]["i1"],
                #                   i["car_number"][j]["i2"],
                #                   i["car_number"][j]["u"],
                #                   ))
                temp_list.append((j, i["car_number"][j]["speed"], i["car_number"][j]["throttle"],
                                  i["car_number"][j]["brake"],
                                  i["car_number"][j]["rpm"],
                                  i["car_number"][j]["gear"],
                                  i["car_number"][j]["gap_to_leader"],
                                  i["car_number"][j]["gap_to_postiion_ahead"],
                                  i["car_number"][j]["updated"],
                                  ))


            temp_list.append(i["timestamp"])  # Append the timestamp to the end of the list.
            big_list.append(temp_list)
            temp_list = []

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


        # Tired right now and cant quite place why this won't work... I am tired evidently. Just get the above working (which was the most intuitive to me.
        # for i in samp["streaming_data"][0]["car_number"]:
        #     print(i, samp["streaming_data"]["car_number"][i]["s"], samp["streaming_data"]["car_number"][i]["r"], samp["streaming_data"]["ts"])



if __name__ == '__main__':
    converter = ConvertDataToList()
    # converter.print_info()
    converter.make_new_json_file()
