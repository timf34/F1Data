from awsiot import mqtt_connection_builder
import boto3
import json
from typing import Dict

from aws_keys import ACCESS_KEY, SECRET_ACCESS_KEY

"""
    Note:
    
    - Omar probably could have told me this, but I won't be able to make this code 
    without also creating some policies on AWS that might take a while... 
    
    Basically only 'things' can subscribe to topics. 
    
    So to do this, I would need to create a 'thing' on AWS, and then create a policy. 
    But thats not worth the time doing right now so I can come back to this again when Omar 
    is with me. 
    
    Doing this would still be generally useful. We could test directly here in code to ensure 
    that our lambda functions (or similar local code to do the same thing) are working correctly, 
    etc.
    
    It would also be super useful for adding tests, to help ensure that the code is working correctly. 
    
    Here is an article/ walkthrough for publishing to mqtt topics, but should bring us most of the way in 
    subscribing to them as well: 
    https://aws.amazon.com/premiumsupport/knowledge-center/iot-core-publish-mqtt-messages-python/
    
    And here is the repo: https://github.com/aws/aws-iot-device-sdk-python-v2
"""


class ReadMQTTChannel:
    """
        This is a class to generally subscribe and listen to the MQTT channel.
    """
    def __init__(self):
        self.iot_client = boto3.client('iot-data',
                                   region_name='us-east-1',
                                   aws_access_key_id=ACCESS_KEY,
                                   aws_secret_access_key=SECRET_ACCESS_KEY)
        self.topic = 'streaming_data'
        self.qos = 1

    def subscribe_to_mqtt_channel(self) -> None:
        # We need to create a 'thing' to get this working.
        pass

    def listen_to_mqtt_channel(self) -> None:
        response = self.client.get_thing_shadow(
            thingName='RaspberryPi'
        )
        print(response)

    def publish_to_mqtt_channel(self, data: Dict) -> None:
        response = self.client.publish(
            topic=self.topic,
            qos=self.qos,
            payload=str(data)
        )
        print(response)


def main():
    read_mqtt_channel = ReadMQTTChannel()
    read_mqtt_channel.subscribe_to_mqtt_channel()
    read_mqtt_channel.listen_to_mqtt_channel()
    read_mqtt_channel.publish_to_mqtt_channel({"test": "test"})


if __name__ == '__main__':
    main()
