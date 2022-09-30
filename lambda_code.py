import json
import boto3
import time
from typing import Dict

# This is just a copy of the lambda code before I went and changed it...

class StreamFromS3:
    def __init__(self, topic="1"):
        self.s3_url: str = 'https://testbucket10022022.s3.eu-west-1.amazonaws.com/very_short_stream_data.json'
        self.s3 = boto3.client('s3')
        self.iot_client = boto3.client('iot-data', region_name='eu-west-1')
        self.key: str = "stream_data.json"
        self.bucket: str = "testbucket10022022"
        self.static_info_key: str = "static_new_json_file.json"
        self.short_loop: bool = True
        self.topic = f"RACE/{topic}"
        print("here's the topic: ", self.topic)

    def get_data(self, get_static_info=False) -> Dict:
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

    def parse_data(self):

        # Get and send the static race day information once initially.
        static_data = self.get_data(get_static_info=True)
        json_object = json.loads(static_data['Body'].read().decode('utf-8'))
        self.publish_to_arduino(json_object)
        time.sleep(4)

        # Now lets process the real race data
        data = self.get_data()
        json_object = json.loads(data['Body'].read().decode('utf-8'))

        for count, info in enumerate(json_object["streaming_data"]):
            # print(f"count: {count} i: {info}")
            self.publish_to_arduino(info)
            time.sleep(0.5)

            if self.short_loop:
                if count == 5:
                    break

    def publish_to_arduino(self, data: Dict):
        print("topic", self.topic)
        response = self.iot_client.publish(
            topic="RACE/1",
            qos=1,
            payload="hey there"
        )


def lambda_handler(event, context):
    topic = event["Requested Topic"]
    topic = topic.replace(".json", "")  # Remove '.json' from string.

    stream_from_s3 = StreamFromS3(topic)
    stream_from_s3.parse_data()

    return ({"data": topic})


