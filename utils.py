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


def main():
    # This function will call the read_json_file function.
    json_list = load_json_file("very_short_stream_data.json")
    print(type(json_list))
    parse_our_json_dict(json_list)


if __name__ == "__main__":
    main()