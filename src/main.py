#!/usr/bin/env python3
import RPi.GPIO as GPIO
from struct import *
from datetime import datetime
import time
import sys
import paho.mqtt.client as mqtt
import glob
import json

if (len(sys.argv) < 8):
   raise  ValueError('Input arguments of mqtt auth and pins not provided')

mqtt_username = str(sys.argv[1])
mqtt_password =  str(sys.argv[2])
mqtt_host = str(sys.argv[3])
mqtt_port = int(sys.argv[4]) 

closed_relay_pin = int(sys.argv[5])
opened_relay_pin = int(sys.argv[6])
closing_relay_pin = int(sys.argv[7])
opening_relay_pin = int(sys.argv[8])

GPIO.setmode (GPIO.BCM)
GPIO.setup(closed_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opened_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(closing_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opening_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

## Temperature
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
client = mqtt.Client()

client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_host, mqtt_port)
client.loop_start()
#device = Device("rpipool","rpipool", "v1","m1","me")
#temp_sensor = Sensor(client, "Temperature", device, "C", icon="mdi:thermometer")

temp_conf = {
    "name": "Pool Temperature",
    "state_topic": "homeassistant/sensor/pool/temperature/state",
    "state_class": "measurement",
    "unit_of_measurement": "C",
    "device_class": "temperature",
    "value_template": "{{ value }}",
    "unique_id": "pool_temperature",
    "device": {
        "identifiers": [
            "pool"
        ],
        "name": "pool",
        "model": "rpi",
        "manufacturer": "me"
    },
    "icon": "mdi:thermometer",
    "platform": "mqtt"
}

cover_conf = {
    "name": "Pool Cover Closed",
    "state_topic": "homeassistant/sensor/pool/cover_closed/state",
    "state_class": "binary",
    "value_template": "{{ value }}",
    "unique_id": "pool_cover_closed",
    "options":[
        "closed",
        "opening",
        "open",
        "closing"
    ],
    "device": {
        "identifiers": [
            "pool"
        ],
        "name": "pool",
        "model": "rpi",
        "manufacturer": "me"
    },
    "platform": "mqtt"
}
client.publish("homeassistant/sensor/pool/temperature/config",json.dumps(temp_conf), 0, True)
client.publish("homeassistant/select/pool/cover/config",json.dumps(cover_conf), 0, True)

while True:
    temp = read_temp()
    cover_closed = GPIO.input(closed_relay_pin) == GPIO.HIGH
    cover_opened = GPIO.input(opened_relay_pin) == GPIO.HIGH
    cover_closing = GPIO.input(closing_relay_pin) == GPIO.HIGH
    cover_opening = GPIO.input(opening_relay_pin) == GPIO.HIGH
    cover_state = "closed"
    #temp_sensor.send(temp)
    client.publish("homeassistant/sensor/pool/temperature/state",str(temp), 0, False)
    client.publish("homeassistant/select/pool/cover/state",cover_state, 0, False)
    time.sleep(6)




