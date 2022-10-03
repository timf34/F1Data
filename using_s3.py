import boto3
import json
import time
from typing import Dict

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY

# TODO: I need to build in an option to just use a local json file here!


class StreamFromS3:
    def __init__(self, filename: str, topic="1"):
        self.s3_url: str = 'https://testbucket10022022.s3.eu-west-1.amazonaws.com/very_short_stream_data.json'
        self.s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)
        self.iot_client = boto3.client('iot-data', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY, region_name='eu-west-1')
        self.key: str = filename
        self.bucket: str = "testbucket10022022"
        self.static_info_key: str = "static_new_json_file.json"
        self.short_loop: bool = True
        self.topic = f"RACE/{topic}"
        print(f"Here is our topic:{self.topic}")
        self.use_timer: bool = False
        self.debugging_timout: int = 4

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
        dict_object = data['Body'].read().decode('utf-8')
        print("dict_object type: ", type(dict_object))
        json_object = json.loads(dict_object)
        print("json_object type: ", type(json_object))

    def parse_through_subsection_of_data_by_time(self, start_time: int, end_time: int, print_data: bool) -> None:
        """
            This function will parse through the data by time, and then publish the data to the arduino.
        """
        data = self.get_data()
        json_object = json.loads(data['Body'].read().decode('utf-8'))
        list_of_data = json_object["streaming_data"]

        end_time *= 2

        list_of_data = list_of_data[start_time:end_time]

        for count, data in enumerate(list_of_data):
            self.publish_to_arduino(data)
            if print_data:
                print(f"count: {count} data: {data}")

    def parse_data(self):
        # Get and send the static race day information once initially.
        static_data = self.get_data(get_static_info=True)
        json_object = json.loads(static_data['Body'].read().decode('utf-8'))

        self.publish_to_arduino(json_object)
        if self.use_timer:
            time.sleep(3)

        # Now lets process the real race data
        data = self.get_data()
        json_object = json.loads(data['Body'].read().decode('utf-8'))

        for count, info in enumerate(json_object["streaming_data"]):
            # print(f"count: {count} i: {info}")
            self.publish_to_arduino(info)
            if self.use_timer:
                time.sleep(0.5)

            if self.short_loop and count == self.debugging_timout:
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
    file_name = "new_json_file.json"
    topic = file_name.replace(".json", "")
    stream_from_s3 = StreamFromS3(filename=file_name, topic=topic)
    stream_from_s3.parse_data()
    # stream_from_s3.parse_through_subsection_of_data_by_time(start_time=0, end_time=10, print_data=True)
