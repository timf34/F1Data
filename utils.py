import json


def load_json_file(filename: str) -> dict:
    # This function will read a json file and return a list of json objects.
    with open(filename, "r") as json_file:
        json_dict = json.load(json_file)
    return json_dict


def parse_our_json_dict(json_dict: dict) -> dict:
    # This function will parse a json dictionary and return a dictionary of
    # the data we want.
    print(json_dict["streaming_data"][0].keys())


def pretty_print_json_to_file(json_dict: dict, filename: str) -> None:
    # This function will pretty print a json dictionary to a file.
    with open(filename, "w") as f:
        json.dump(json_dict, f, indent=4)


def remove_keys_from_nested_json_dict(json_dict: dict, keys: list) -> dict:
    # This function will remove keys from a json dictionary, that might have nested dictionaries.
    for key in keys:
        if key in json_dict:
            del json_dict[key]
        else:
            for k, v in json_dict.items():
                if isinstance(v, dict):
                    # Using recursion... woohoo :)
                    remove_keys_from_nested_json_dict(v, keys)
    return json_dict


def main():
    # This function will call the read_json_file function.
    # json_list = load_json_file("data/very_short_stream_data.json")
    # print(type(json_list))
    # parse_our_json_dict(json_list)
    json_dict = load_json_file("data/temp_data.json")
    json_dict = remove_keys_from_nested_json_dict(json_dict, ["Line", "Tla", "FirstName",
                                                              "LastName", "BroadcastName", "TeamColour"])
    pretty_print_json_to_file(json_dict, "data/temp_data_pretty.json")


if __name__ == "__main__":
    main()