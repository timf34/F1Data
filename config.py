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

