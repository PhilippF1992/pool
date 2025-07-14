import json
import glob
import time
import paho.mqtt.client as mqtt
from ..device import *

class DS18B20():
    def __init__(self, name, uniq_id, device: Device, client: mqtt.Client):
        self.name = name
        self.device = device
        self.client = client
        self.uniq_id = uniq_id
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
        self.file = device_file
        self.send_config()

    def send_config(self):
        conf = {
            "name": self.name,
            "state_topic": "homeassistant/sensor/" + self.device.name + "/" + self.uniq_id + "/state",
            "state_class": "measurement",
            "unit_of_measurement": "C",
            "device_class": "temperature",
            "value_template": "{{ value }}",
            "unique_id": self.uniq_id,
            "device": self.device,
            "icon": "mdi:thermometer",
            "platform": "mqtt"
        }
        self.client.publish("homeassistant/sensor/" + self.device.name + "/" + self.uniq_id + "/config",json.dumps(conf), 0, True)
        self.send_data()
    
    def send_data(self):
        self.client.publish("homeassistant/sensor/" + self.device.name + "/" + self.uniq_id + "/state", str(self._read_data()), 0, False)

    def _read_temp_raw(self):
        f = open(self.file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _read_data(self):
        lines = self._read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c