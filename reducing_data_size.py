import json
from config import TEST_CASE_SINGLE_TIMESTAMP_TWO_CARS_SHORT_KEYS, TEST_CASE_SINGLE_TIMESTAMP_TWENTY_CARS_SHORT_KEYS

# json_obj = json.dumps(TEST_CASE_SINGLE_TIMESTAMP_TWO_CARS_SHORT_KEYS, indent=4)
# print(len(json_obj))


# I might want to inherit from pytest or something similar.
class LetsTestJsonReductionStuff(object):
    def __init__(self):
        self.test1 = TEST_CASE_SINGLE_TIMESTAMP_TWO_CARS_SHORT_KEYS
        self.test2 = TEST_CASE_SINGLE_TIMESTAMP_TWENTY_CARS_SHORT_KEYS

    def test_no_indent(self):
        with_indent1 = json.dumps(self.test1, indent=4)
        with_indent2 = json.dumps(self.test2, indent=4)

        without_indent1 = json.dumps(self.test1)
        without_indent2 = json.dumps(self.test2)

        print("Testing no indent...")
        print("With indent 1: ", len(with_indent1))
        print("With indent 2: ", len(with_indent2))
        print("Without indent 1: ", len(without_indent1))
        print("Without indent 2: ", len(without_indent2))
        print("")

        assert len(with_indent1) > len(without_indent1)
        assert len(with_indent2) > len(without_indent2)

    def test_test_cases(self):
        self.test_no_indent()


if __name__ == "__main__":
    LetsTestJsonReductionStuff().test_test_cases()
