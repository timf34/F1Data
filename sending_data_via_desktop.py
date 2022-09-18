import asyncio
import json
import websocket
from websockets import connect

from typing import Dict
from utils import load_json_file, parse_our_json_dict

# This file reads through the json file by file, and then sends the information to the deivce via AWS API Gateway
# Plan
# - Read through the json file
# - Send the information to the device via AWS API Gateway


class SendData:
    def __init__(self):
        self.json_file: Dict = load_json_file("data/short_stream_data.json")  # Note that this is a dict and not a json object
        self.websocket_uri: str = 'wss://rcfqvfjypd.execute-api.eu-west-1.amazonaws.com/production'

    def print_info(self):
        print("size of json file: ", len(json.dumps(self.json_file)))
        print("type of json file: ", type(self.json_file))

    def iterate_list(self):

        # Get the list
        json_list = self.json_file["streaming_data"]
        print("size of json list: ", len(json.dumps(json_list)))

        # Iterate through the list for first 3 items
        for i in range(3):
            print("item: ", i)
            print("type of item: ", type(json_list[i]))
            print("item: ", json_list[i])
            print("keys: ", json_list[i].keys())
            print("values: ", json_list[i].values())
            print("")

    def send_data(self):
        uri = self.websocket_uri


async def hello(uri):
    async with connect(uri) as websocket:
        await websocket.send(json.dumps({"action": "sendMessage", "message": "this is working"}))
        await websocket.recv()


if __name__ == "__main__":
    send_data = SendData()
    send_data.print_info()
    # send_data.iterate_list()
    asyncio.run(hello(send_data.websocket_uri))

    # ws = websocket.WebSocket()
    # ws.connect("wss://rcfqvfjypd.execute-api.eu-west-1.amazonaws.com/production")
    # ws.send("Hello, Server")


