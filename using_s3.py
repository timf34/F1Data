import boto3
import json
import sys

from typing import Dict

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY


class StreamFromS3:
    def __init__(self):
        self.s3_url: str = 'https://testbucket10022022.s3.eu-west-1.amazonaws.com/very_short_stream_data.json'
        self.s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)
        self.iot_client = boto3.client('iot-data', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY, region_name='eu-west-1')
        self.key: str = "stream_data.json"
        self.bucket: str = "testbucket10022022"
        self.static_info_key: str = "static_new_json_file.json"

    def get_data(self, get_static_info=False) -> Dict:
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

        json_object = json.loads(dict_object)
        print("json_object type: ", type(json_object))

    def parse_data(self):

        # Get and send the static race day information once initially.
        static_data = self.get_data(get_static_info=True)
        json_object = json.loads(static_data['Body'].read().decode('utf-8'))
        # print(sys.getsizeof(json_object), type(json_object))

        # data = self.get_data()
        # json_object = json.loads(data['Body'].read().decode('utf-8'))
        # print(json_object["streaming_data"][0].keys())
        #
        # for count, info in enumerate(json_object["streaming_data"]):
        #     print(f"count: {count} i: {info}")
        #
        #     response = self.iot_client.publish(
        #         topic="PreMatch/420",
        #         qos=1,
        #         payload=str(info)
        #     )
        #     print("response: ", response)
        #
        #     if count == 5:
        #         break

    # TODO: do this line locally `iotClient = client = boto3.client('iot-data', region_name='eu-west-1')` and publish

    @staticmethod
    def _pass():
        pass




if __name__ == '__main__':
    stream_from_s3 = StreamFromS3()
    # stream_from_s3.get_data()
    # stream_from_s3.print_data()
    stream_from_s3.parse_data()
