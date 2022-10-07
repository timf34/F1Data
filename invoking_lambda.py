import boto3
import json

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY


class InvokeLambda:
    def __init__(self):
        self.lambda_client = boto3.client('lambda', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_ACCESS_KEY, region_name='eu-west-1')
        self.payload: str = json.dumps({"Requested Topic": "new_json_file_with_lap_times_4fps.json"})
        self.function_name: str = "arn:aws:lambda:eu-west-1:500871178580:function:preRaceS3Grab"

    def invoke_lambda(self):
        response = self.lambda_client.invoke(
            FunctionName=self.function_name,
            InvocationType="RequestResponse",
            Payload=self.payload
        )
        print(response)




def main():
    invoke_lambda = InvokeLambda()
    invoke_lambda.invoke_lambda()

if __name__ == '__main__':
    main()
    print("Done.")