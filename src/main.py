#!/usr/bin/env python3
import RPi.GPIO as GPIO
from struct import *
from datetime import datetime
import time
import sys
import paho.mqtt.client as mqtt
import glob
import json

if (len(sys.argv) < 9):
   raise  ValueError('Input arguments of mqtt auth and pins not provided')

mqtt_username = str(sys.argv[1])
mqtt_password =  str(sys.argv[2])
mqtt_host = str(sys.argv[3])
mqtt_port = int(sys.argv[4]) 

closed_relay_pin = int(sys.argv[5])
opened_relay_pin = int(sys.argv[6])
closing_relay_pin = int(sys.argv[7])
opening_relay_pin = int(sys.argv[8])
impuls_pin = int(sys.argv[9])

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(closed_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opened_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(closing_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opening_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(impuls_pin, GPIO.OUT)
GPIO.output(impuls_pin, GPIO.LOW)

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

def on_message(client, userdata, message):
    payload=str(message.payload.decode("utf-8"))
    if (payload=="True" and message.topic=="homeassistant/switch/pool/cover_impuls/set"):
        client.publish("homeassistant/switch/pool/cover_impuls/state",str(True), 0, False)
        GPIO.output(impuls_pin, GPIO.HIGH)
        time.sleep(1)
        client.publish("homeassistant/switch/pool/cover_impuls/state",str(False), 0, False)
        GPIO.output(impuls_pin, GPIO.LOW)

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

cover_closed_conf = {
    "name": "Pool Cover Closed",
    "state_topic": "homeassistant/binary_sensor/pool/cover_closed/state",
    "state_class": "binary",
    "value_template": "{{ value }}",
    "unique_id": "pool_cover_closed",
    "payload_off":"False",
    "payload_on":"True",
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
cover_opened_conf = {
    "name": "Pool Cover Opened",
    "state_topic": "homeassistant/binary_sensor/pool/cover_opened/state",
    "state_class": "binary",
    "value_template": "{{ value }}",
    "unique_id": "pool_cover_opened",
    "payload_off":"False",
    "payload_on":"True",
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
cover_closing_conf = {
    "name": "Pool Cover Closing",
    "state_topic": "homeassistant/binary_sensor/pool/cover_closing/state",
    "state_class": "binary",
    "value_template": "{{ value }}",
    "unique_id": "pool_cover_closing",
    "payload_off":"False",
    "payload_on":"True",
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
cover_opening_conf = {
    "name": "Pool Cover Opening",
    "state_topic": "homeassistant/binary_sensor/pool/cover_opening/state",
    "state_class": "binary",
    "value_template": "{{ value }}",
    "unique_id": "pool_cover_opening",
    "payload_off":"False",
    "payload_on":"True",
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
cover_impuls_conf = {
    "name": "Pool Cover Impuls",
    "state_topic": "homeassistant/switch/pool/cover_impuls/state",
    "command_topic": "homeassistant/switch/pool/cover_impuls/set",
    "state_class": "binary",
    "value_template": "{{ value }}",
    "unique_id": "pool_cover_impuls",
    "payload_off":"False",
    "payload_on":"True",
    "state_off":"False",
    "state_on":"True",
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

client = mqtt.Client()
client.on_message=on_message
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_host, mqtt_port)
client.loop_start()
client.publish("homeassistant/sensor/pool/temperature/config",json.dumps(temp_conf), 0, True)
client.publish("homeassistant/binary_sensor/pool/cover_closed/config",json.dumps(cover_closed_conf), 0, True)
client.publish("homeassistant/binary_sensor/pool/cover_opened/config",json.dumps(cover_opened_conf), 0, True)
client.publish("homeassistant/binary_sensor/pool/cover_closing/config",json.dumps(cover_closing_conf), 0, True)
client.publish("homeassistant/binary_sensor/pool/cover_opening/config",json.dumps(cover_opening_conf), 0, True)
client.publish("homeassistant/switch/pool/cover_impuls/config",json.dumps(cover_impuls_conf), 0, True)
client.publish("homeassistant/switch/pool/cover_impuls/state",str(False), 0, False)
client.subscribe("homeassistant/switch/pool/cover_impuls/set")

while True:
    temp = read_temp()
    cover_closed = GPIO.input(closed_relay_pin) == GPIO.HIGH
    cover_opened = GPIO.input(opened_relay_pin) == GPIO.HIGH
    cover_closing = GPIO.input(closing_relay_pin) == GPIO.HIGH
    cover_opening = GPIO.input(opening_relay_pin) == GPIO.HIGH

    client.publish("homeassistant/sensor/pool/temperature/state",str(temp), 0, False)
    client.publish("homeassistant/binary_sensor/pool/cover_closed/state",str(cover_closed), 0, False)
    client.publish("homeassistant/binary_sensor/pool/cover_opened/state",str(cover_opened), 0, False)
    client.publish("homeassistant/binary_sensor/pool/cover_closing/state",str(cover_closing), 0, False)
    client.publish("homeassistant/binary_sensor/pool/cover_opening/state",str(cover_opening), 0, False)
    time.sleep(6)




