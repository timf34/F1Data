#sample_dict = {}
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