import json
import requests

from datetime import datetime
from sseclient import SSEClient
from Client.constants import BASE_URL

def get_response(url):
    return requests.get(url, preload_content=False)

class from_dict:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def receive_event(event, type):
    with open("./dicts/notifications.json", "r") as f:
        load = json.load(f)
        load.append({
            "type": type,
            "date": datetime.now(),
            "data": event.dict()
        })
    with open("./dicts/notifications.json", "w") as f:
        json.dump(load, f)

response = get_response(BASE_URL + '/events')
client = SSEClient(response)
while len(client.events()) != 0:
    for i in client.events():
        i = json.loads(i)
        receive_event(from_dict(i['event']), i['type'])

