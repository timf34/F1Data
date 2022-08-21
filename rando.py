sample_dict = {}
big_list = []

sample_dict = {"a": 1, "b": 2, "c": 3}

for key, value in sample_dict.items():
    print(key, value)
    big_list.append(sample_dict.copy())
    sample_dict["a"] += 3
    sample_dict["b"] += 3
    sample_dict["c"] += 3
    print(big_list)


print(big_list)