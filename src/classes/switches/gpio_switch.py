import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from ..device import *

class GPIO_Switch:
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, pin, connect_on, parent= ""):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.pin = pin
        self.connect_on = connect_on
        if (parent == ""):
            self.topic = "homeassistant/switch/" + self.device.name + "/" + self.uniq_id
        else: 
            self.topic = "homeassistant/switch/" + self.device.name + "_" + parent + "/" + self.uniq_id
        if (GPIO.HIGH == connect_on):
            self.disconnect_on = GPIO.LOW
        else:
            self.disconnect_on = GPIO.HIGH

        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, self.disconnect_on)
        self._send_config()

    def _send_config(self):
        conf = {
            "name": self.name,
            "state_topic": self.topic + "/state",
            "command_topic": self.topic + "/set",
            "state_class": "binary",
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id,
            "device": self.device,
            "payload_off":"False",
            "payload_on":"True",
            "state_off":"False",
            "state_on":"True",
            "platform": "mqtt"
        }
        self.client.publish(self.topic + "/config",json.dumps(conf), 0, True)
        self._send_data(False)

    def _send_data(self, data):
        self.client.publish(self.topic + "/state", str(data), 0, False)

    def set_off(self):
        self._send_data(False)
        GPIO.output(self.pin, self.disconnect_on)

    def set_on(self):
        self._send_data(True)
        GPIO.output(self.pin, self.connect_on)

    def subscribe(self):
        self.client.subscribe(self.topic + "/set")

    def on_message(self, client, userdata, message):
        if (message.topic == self.topic + "/set"):
            payload=str(message.payload.decode("utf-8"))
            if (payload == "True"):
                self.set_on
            else: 
                self.set_off

