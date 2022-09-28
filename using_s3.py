import boto3
import json
import time
import sys

from typing import Dict

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY


# TODO: need to add the topic to the code here now... probs with a post init function.
class StreamFromS3:
    def __init__(self, topic="1"):
        self.s3_url: str = 'https://testbucket10022022.s3.eu-west-1.amazonaws.com/very_short_stream_data.json'
        self.s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)
        self.iot_client = boto3.client('iot-data', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY, region_name='eu-west-1')
        self.key: str = "stream_data.json"
        self.bucket: str = "testbucket10022022"
        self.static_info_key: str = "static_new_json_file.json"
        self.short_loop: bool = True
        self.topic = f"RACE/{topic}"
        self.use_timer: bool = False

    def get_data(self, get_static_info=False) -> Dict:
        # Note that data["Body"] is of type: botocore.response.StreamingBody
        if get_static_info:
            return self.s3.get_object(Bucket=self.bucket, Key=self.static_info_key)
        return self.s3.get_object(Bucket=self.bucket, Key=self.key)

    def print_data(self):
        data = self.get_data()
        print("type of data: ", type(data))
        print("data: ", data)
        print("data['Body']: ", data['Body'])

        # print(next(data["Body"]))  # This prints like this: b'{\r\n    "streaming_data": [\r\n        {\r\n            "car_number": {\r\n                "44": {\r\n                    "s": 228,\r\n                    "t": 100,\r\n

        # print(next(data["Body"]).decode('utf-8'))  # This prints like a real json file... but it gets cut off early. It only reads the first 1000 bytes
        #for i in data["Body"].iter_lines():
        #    print(i.decode('utf-8'))

        # Even this is also pretty fast...
        # print("data['Body'].read(): ", data['Body'].read().decode('utf-8'))  # This prints like a real json file... but it gets cut off early. It only reads the first 1000 bytes

        # Now lets try to load it into a json object
        # json_object = json.loads(data['Body'].read())
        # print("json_object: ", json_object)
        # print("type of json_object: ", type(json_object))
        # print("size of json object: ", len(json_object))
        # if type(json_object) is dict:
        #     print("the size is actually: ", sys.getsizeof(json_object))

        dict_object = data['Body'].read().decode('utf-8')
        print("dict_object type: ", type(dict_object))
        # print(dict_object[:1000])

        json_object = json.loads(dict_object)
        print("json_object type: ", type(json_object))

    def parse_through_subsection_of_data_by_time(self, start_time: int, end_time: int):
        data = self.get_data()
        json_object = json.loads(data['Body'].read().decode('utf-8'))
        list_of_data = json_object["streaming_data"]

        # Note: we don't actually do this as we are using list indices rather than the actual timestamps.
        # Account for the offset of 1993 seconds, for this dataset at least
        # start_time += 1993
        # end_time = (end_time * 2) + 1993  # Double it to account for the fact that we use half seconds in the data

        end_time *= 2

        list_of_data = list_of_data[start_time:end_time]
        for count, data in enumerate(list_of_data):
            pass

    def parse_data(self):
        # Get and send the static race day information once initially.
        static_data = self.get_data(get_static_info=True)
        json_object = json.loads(static_data['Body'].read().decode('utf-8'))
        # print(sys.getsizeof(json_object), type(json_object))  # Size is 232
        self.publish_to_arduino(json_object)
        if self.use_timer:
            time.sleep(3)

        # Now lets process the real race data
        data = self.get_data()
        json_object = json.loads(data['Body'].read().decode('utf-8'))
        # print(json_object["streaming_data"][0].keys())

        for count, info in enumerate(json_object["streaming_data"]):
            # print(f"count: {count} i: {info}")
            self.publish_to_arduino(info)
            if self.use_timer:
                time.sleep(0.5)

            if self.short_loop and count == 3:
                break

    def publish_to_arduino(self, data: Dict):
        response = self.iot_client.publish(
            topic=self.topic,
            qos=1,
            payload=str(data)
        )

    def work_with_data(self):
        data = self.get_data()
        print(data)
        print(type(data["Body"]))


if __name__ == '__main__':
    stream_from_s3 = StreamFromS3()
    # stream_from_s3.get_data()
    # stream_from_s3.print_data()
    stream_from_s3.parse_data()
    # stream_from_s3.work_with_data()
    # stream_from_s3.parse_through_subsection_of_data_by_time(0, 10)
