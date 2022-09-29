import json

# sample_dict = {}
# big_list = []
#
# sample_dict = {"a": 1, "b": 2, "c": 3}
#
# for key, value in sample_dict.items():
#     print(key, value)
#     big_list.append(sample_dict.copy())
#     sample_dict["a"] += 3
#     sample_dict["b"] += 3
#     sample_dict["c"] += 3
#     print(big_list)
#
#
# print(big_list)

# For loop that increments by the value of 0.5

def trying_for_loops():
    for i in range(0, 10, 1):
        if i == 0:
            pass
        else:
            print(i/2)

    starting = 2001.5
    enidng = 2004.5

    # increment between starting and ending in 0.5 increments
    for i in range(int(starting*2 + 1), int(enidng*2)):
        print(i/2)


def trying_to_parse_json_file_by_time():
    # Open json file
    with open(r"C:\Users\timf3\PycharmProjects\f1Data\data\stream_data_short_keys.json", "r") as file:
        data = json.load(file)
        list_of_data = data["streaming_data"]

        # Note that the start time effectively starts from 1993 seconds!

        list_of_data = list_of_data[0:15]

        for count, data in enumerate(list_of_data):
            print(f"count: {count} data: {data}")

def main():
    trying_to_parse_json_file_by_time()

if __name__ == "__main__":
    main()
