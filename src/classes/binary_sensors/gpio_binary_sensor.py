import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from ..device import *

class GPIO_Binary_Sensor():
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client, pin, parent= ""):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        self.pin = pin
        if (parent == ""):
            self.topic = "homeassistant/binary_sensor/" + self.device.name + "/" + self.uniq_id
        else: 
            self.topic = "homeassistant/binary_sensor/" + self.device.name + "_" + parent + "/" + self.uniq_id
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self._send_config()

    def _send_config(self):
        conf = {
            "name": self.name,
            "state_topic": self.topic + "/state",
            "state_class": "binary",
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id,
            "device": self.device,
            "payload_off":"False",
            "payload_on":"True",
            "platform": "mqtt"
        }
        self.client.publish(self.topic + "/config",json.dumps(conf), 0, True)
    
    def send_data(self):
        self.client.publish(self.topic + "/state", str(self._read_data()), 0, False)

    def _read_data(self):
        return GPIO.input(self.pin) == GPIO.HIGH