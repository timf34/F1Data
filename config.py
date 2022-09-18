from dataclasses import dataclass
from typing import List


@dataclass
class F1DataConfig:
    # Note: I need to figure out what I want to store here
    # Length of our dataset:
    # very short and full seem like the two most useful categories, so a simple bool should do

    # I also will want the name of our generated json file to depend on whether its full or super short.

    # There should maybe also be a list of the cars... and this again depends on another bool for whether we want to
    # use the full list of cars or not.
    # I think there should be a post process or post init variable.

    full_dataset: bool = False  # Whether to use the full dataset or not (i.e. all the race, or only 40ish seconds)
    full_list_of_cars: bool = False  # Whether to use all cars or just the first two (chosen arbitrarily)

    def __post_init__(self):
        if self.full_list_of_cars:
            self.list_of_cars: List[str] = ['44', '77', '33', '5', '16', '10', '20', '55', '26', '8',
                                            '23', '3', '27', '7', '11', '99', '63', '88', '18', '4']
        else:
            self.list_of_cars: List[str] = ['44', '77']


# We will also use this page to define different dicts, for testing how we can reduce their size

TEST_CASE_SINGLE_TIMESTAMP_TWO_CARS_SHORT_KEYS = {
    "streaming_data":
    [
        {
            "car_number": {
                "44": {
                    "s": 228,
                    "t": 100,
                    "b": "False",
                    "r": 11135,
                    "g": 5,
                    "i1": "+0.020",
                    "i2": "+0.020",
                    "u": "True"
                },
                "77": {
                    "s": 228,
                    "t": 100,
                    "b": "False",
                    "r": 10747,
                    "g": 6,
                    "i1": "LAP 1",
                    "i2": "LAP 1",
                    "u": "True"
                }
            },
            "ts": 1993
        }
    ]
}

TEST_CASE_SINGLE_TIMESTAMP_TWENTY_CARS_SHORT_KEYS = {
    "streaming_data":
    [
        {
            "car_number": {
                "44": {
                    "s": 228,
                    "t": 100,
                    "b": "False",
                    "r": 11135,
                    "g": 5,
                    "i1": "+0.020",
                    "i2": "+0.020",
                    "u": "True"
                },
                "77": {
                    "s": 228,
                    "t": 100,
                    "b": "False",
                    "r": 10747,
                    "g": 6,
                    "i1": "LAP 1",
                    "i2": "LAP 1",
                    "u": "True"
                },
                "33": {
                    "s": 227,
                    "t": 100,
                    "b": "False",
                    "r": 10648,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "5": {
                    "s": 239,
                    "t": 100,
                    "b": "False",
                    "r": 11130,
                    "g": 6,
                    "i1": "+0.158",
                    "i2": "+0.138",
                    "u": "True"
                },
                "16": {
                    "s": 231,
                    "t": 100,
                    "b": "False",
                    "r": 10912,
                    "g": 6,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "10": {
                    "s": 226,
                    "t": 100,
                    "b": "False",
                    "r": 10932,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "20": {
                    "s": 227,
                    "t": 100,
                    "b": "False",
                    "r": 10619,
                    "g": 6,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "55": {
                    "s": 238,
                    "t": 99,
                    "b": "False",
                    "r": 11071,
                    "g": 6,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "26": {
                    "s": 232,
                    "t": 100,
                    "b": "False",
                    "r": 10691,
                    "g": 6,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "8": {
                    "s": 229,
                    "t": 100,
                    "b": "False",
                    "r": 10939,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "23": {
                    "s": 228,
                    "t": 100,
                    "b": "False",
                    "r": 10745,
                    "g": 6,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "3": {
                    "s": 230,
                    "t": 100,
                    "b": "False",
                    "r": 11170,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "27": {
                    "s": 0,
                    "t": 25,
                    "b": "False",
                    "r": 11020,
                    "g": 1,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "7": {
                    "s": 227,
                    "t": 100,
                    "b": "False",
                    "r": 10551,
                    "g": 6,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "11": {
                    "s": 228,
                    "t": 100,
                    "b": "False",
                    "r": 11963,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "99": {
                    "s": 227,
                    "t": 100,
                    "b": "False",
                    "r": 12199,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "63": {
                    "s": 231,
                    "t": 100,
                    "b": "False",
                    "r": 12046,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "88": {
                    "s": 230,
                    "t": 100,
                    "b": "False",
                    "r": 11930,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "18": {
                    "s": 228,
                    "t": 100,
                    "b": "False",
                    "r": 11939,
                    "g": 5,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                },
                "4": {
                    "s": 232,
                    "t": 99,
                    "b": "False",
                    "r": 10968,
                    "g": 6,
                    "i1": "NaN",
                    "i2": "NaN",
                    "u": "True"
                }
            },
            "ts": 1993
        }
    ]
}

TEST_CASE_SINGLE_TIMESTAMP_TWO_CARS_LIST = {
    "streaming_data":
    [228, 100, "False", 11135, 5, "+0.020", "+0.020", "True",
     228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
     1993
    ]
}


TEST_CASE_SINGLE_TIMESTAMP_TWENTY_CARS_LIST = {
    "streaming_data":
    [228, 100, "False", 11135, 5, "+0.020", "+0.020", "True",
     228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
    228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True",
     1993
    ]
}

TEST_CASE_SINGLE_TIMESTAMP_TWENTY_CARS_LIST_2D = {
    "streaming_data":
    [
        [228, 100, "False", 11135, 5, "+0.020", "+0.020", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],
        [1993]
    ]
}

FOR_AWS = {
    "streaming_data":
    [
        [228, 100, "False", 11135, 5, "+0.020", "+0.020", "True"],  [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],  [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],[228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],[228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],[228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],  [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"], [228, 100, "False", 10747, 6, "LAP 1", "LAP 1", "True"],  [1993]
    ]
}
