import socket
import time
import json
from .device import *
import paho.mqtt.client as mqtt


color_map = {
    0: "Warm white", 
    1: "White", 
    2: "Blue", 
    3: "Lagoon",
    4: "Cyan", 
    5: "Purple", 
    6: "Magenta", 
    7: "Pink",
    8: "Red", 
    9: "Orange", 
    10: "Green",
    16: "Gradient", 
    17: "Rainbow", 
    18: "Parade",
    19: "Techno", 
    20: "Horizon", 
    21: "Hazard", 
    22: "Magical"
}

brightness_map = {
    0: "Low", 
    1: "Medium", 
    2: "Strong", 
    3: "Maximum"
}

speed_map = {
    0: "Slow", 
    1: "Medium", 
    2: "Fast"
}
state_map = {
    0: "False",
    2: "True"
}

class Light:
    def __init__(self, uniq_id, device: Device, client: mqtt.Client, ip, port):
        self.uniq_id = uniq_id
        self.ip = ip
        self.port = port
        self.device = device
        self.client = client
        self.color_topic = "homeassistant/select/" + self.device.name + "_" + uniq_id + "/" + "color"
        self.brightness_topic = "homeassistant/select/" + self.device.name + "_" + uniq_id + "/" + "brightness"
        self.speed_topic = "homeassistant/select/" + self.device.name + "_" + uniq_id + "/" + "speed"
        self.state_topic = "homeassistant/switch/" + self.device.name + "_" + uniq_id + "/" + "state"

    def send_tcp_message(self, message = ""):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            sock.connect((self.ip, self.port))
            sock.sendall(message.encode())
            response = sock.recv(1024).decode()
            return response
        
    def set_current_state(self):
        response = self.send_tcp_message()
        speed = int(response[70:71], 16) - 4
        if speed <= 0: 
            speed = 0
        self.speed = speed
        self.color = int(response[64:66], 16)
        self.brightness = int(response[71:72], 16) // 4
        self.state = int(response[33:34])


    def send_command(self, command: dict):
        message = json.dumps(command)
        self.send_tcp_message(message)

    def send_config(self):
        self._send_config_color()
        self._send_config_speed()
        self._send_config_brightness()
        self._send_config_state()
        self._send_data_mqqt()

    def _send_config_color(self):
        conf = {
            "name": "color",
            "state_topic": self.color_topic + "/state",
            "command_topic": self.color_topic + "/select",
            "value_template": "{{ value }}",
            "unique_id": "color",
            "device": self.device,
            "options": list(color_map.values()),
            "platform": "mqtt"
        }
        self.client.publish(self.color_topic + "/config",json.dumps(conf), 0, True)

    def _send_data_color(self):
        self.client.publish(self.color_topic + "/state", str(color_map.get(self.color, "Error")), 0, False)

    def _send_config_brightness(self):
        conf = {
            "name": "brightness",
            "state_topic": self.brightness_topic + "/state",
            "command_topic": self.brightness_topic + "/select",
            "value_template": "{{ value }}",
            "unique_id": "brightness",
            "device": self.device,
            "options": list(brightness_map.values()),
            "platform": "mqtt"
        }
        self.client.publish(self.brightness_topic + "/config",json.dumps(conf), 0, True)

    def _send_data_brightness(self):
        self.client.publish(self.brightness_topic + "/state", str(brightness_map.get(self.brightness, "Error")), 0, False)

    def _send_config_speed(self):
        conf = {
            "name": "speed",
            "state_topic": self.speed_topic + "/state",
            "command_topic": self.speed_topic + "/select",
            "value_template": "{{ value }}",
            "unique_id": "speed",
            "device": self.device,
            "options": list(speed_map.values()),
            "platform": "mqtt"
        }
        self.client.publish(self.speed_topic + "/config",json.dumps(conf), 0, True)

    def _send_data_speed(self):
        self.client.publish(self.speed_topic + "/state", str(speed_map.get(self.speed, "Error")), 0, False)

    def _send_config_state(self):
        conf = {
            "name": "state",
            "state_topic": self.state_topic + "/state",
            "command_topic": self.state_topic + "/set",
            "state_class": "binary",
            "value_template": "{{ value }}",
            "unique_id": "state",
            "device": self.device,
            "payload_off":"False",
            "payload_on":"True",
            "state_off":"False",
            "state_on":"True",
            "platform": "mqtt"
        }
        self.client.publish(self.state_topic + "/config",json.dumps(conf), 0, True)

    def _send_data_state(self):
        self.client.publish(self.state_topic + "/state", str(state_map.get(self.state, "Error")), 0, False)

    def _send_data_mqqt(self):
        self.set_current_state()
        self._send_data_state()
        self._send_data_color()
        self._send_data_brightness()
        self._send_data_speed()

    def _set_state(self, state):
        self.send_command({"sprj":state})
        self._send_data_mqqt()

    def _set_color(self, color):
        self.send_command({"prcn":color})
        self._send_data_mqqt()

    def _set_brightness(self, brightness):
        self.send_command({"plum":brightness})
        self.send_command({"prcn":self.color})
        self._send_data_mqqt()

    def _set_speed(self, speed):
        self.send_command({"pspd":speed})
        self.send_command({"prcn":self.color})
        self._send_data_mqqt()

    def subscribe(self):
        self.client.subscribe(self.state_topic + "/set")
        self.client.subscribe(self.color_topic + "/select")
        self.client.subscribe(self.speed_topic + "/select")
        self.client.subscribe(self.brightness_topic + "/select")
        self._send_data_mqqt()

    def _translate_back(self,options, option):
        for key, value in options.items():
            if value == option:
                return key

    def on_message(self, message):
        payload=str(message.payload.decode("utf-8"))
        if("state/" in message.topic):
            new_state = self._translate_back(state_map, payload)
            self._set_state(new_state)
        if("color" in message.topic):
            new_color = self._translate_back(color_map, payload)
            self._set_color(new_color)
        if("brightness" in message.topic):
            new_brightness = self._translate_back(brightness_map, payload)
            self._set_brightness(new_brightness)
        if("speed" in message.topic):
            new_speed = self._translate_back(speed_map, payload)
            self._set_speed(new_speed)