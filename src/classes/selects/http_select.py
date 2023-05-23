import json
import paho.mqtt.client as mqtt
from ..device import *

class HTTP_Select:
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, endpoint, options, default, parent= ""):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.endpoint = endpoint
        self.options = options
        self.default = default
        if (parent == ""):
            self.topic = "homeassistant/select/" + self.device.name + "/" + self.uniq_id
        else: 
            self.topic = "homeassistant/select/" + self.device.name + "_" + parent + "/" + self.uniq_id
        self._send_config()

    def _send_config(self):
        conf = {
            "name": self.name,
            "state_topic": self.topic + "/state",
            "command_topic": self.topic + "/select",
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id,
            "device": self.device,
            "options": self.options,
            "platform": "mqtt"
        }
        self.client.publish(self.topic + "/config",json.dumps(conf), 0, True)
        self._send_data(self.default)

    def _send_data(self, option):
        self.client.publish(self.topic + "/state", str(option), 0, False)

    def set(self, option):
        self._send_data(option)

    def subscribe(self):
        self.client.subscribe(self.topic + "/select")

    def on_message(self, client, userdata, message):
        if (message.topic == self.topic + "/select"):
            payload=str(message.payload.decode("utf-8"))
            self.set(payload)

