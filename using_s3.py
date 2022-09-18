import boto3
import json
import sys

ACCESS_KEY = 'AKIAXJHR7VFKNE7DRJF7'
SECRET_ACCESS_KEY = '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'


class StreamFromS3:
    def __init__(self):
        self.s3_url: str = 'https://testbucket10022022.s3.eu-west-1.amazonaws.com/very_short_stream_data.json'
        self.s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY)
        self.key = "stream_data.json"
        self.bucket = "testbucket10022022"

    def get_data(self):
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



if __name__ == '__main__':
    stream_from_s3 = StreamFromS3()
    # stream_from_s3.get_data()
    stream_from_s3.print_data()

