import boto3

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
        print(next(data["Body"]))

if __name__ == '__main__':
    stream_from_s3 = StreamFromS3()
    # stream_from_s3.get_data()
    stream_from_s3.print_data()

