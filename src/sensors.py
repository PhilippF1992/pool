#!/usr/bin/env python3
from struct import *
from datetime import datetime
import time
import sys
import subprocess
import paho.mqtt.client as mqtt
import os
import glob

if (len(sys.argv) < 8):
   raise  ValueError('Input arguments of mqtt auth and pins not provided')

mqtt_username = str(sys.argv[1])
mqtt_password =  str(sys.argv[2])
mqtt_host = str(sys.argv[3])
mqtt_port = str(sys.argv[4]) 

closed_relay_pin = int(sys.argv[5])
opened_relay_pin = int(sys.argv[6])
closing_relay_pin = int(sys.argv[7])
opening_relay_pin = int(sys.argv[8])

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
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
    
#******************************************
# Callback function when the client successfully connects to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    while True:
      temp = read_temp()
      cover_state = "closed"

      base_topic_temp = "homeassistant/sensor/pool/temperature/"
      base_topic_cover = "homeassistant/sensor/pool/cover/"

      # Publish temp config
      config_payload_temp = {
          "name": "Pool Temperature",
          "state_topic": base_topic_temp + "state",
          "state_class": "measurement",
          "unit_of_measurement": "°C",
          "device_class": "temperature",
          "value_template": "{{ value }}",
          "unique_id": "pool_temperature",
          "device": {
            "identifiers": [
               "pool_temperature_sensor"
            ],
            "name": "Pool Temperature",
            "model": "None",
            "manufacturer": "None"
          },
          "icon": "mdi:thermometer",
          "platform": "mqtt"
      }
      client.publish(topic=base_topic_temp + "config", payload=str(config_payload_temp), qos=0, retain=False)

      # Publish cover config
      #config_payload_cover = {
      #    "name": "Pool Cover",
      #    "state_topic": base_topic_cover + "state",
      #    "state_class": "measurement",
      #    "unit_of_measurement": "C",
      #    "device_class": "Temperature",
      #    "value_template": "{{ value }}",
      #    "unique_id": "pool_temperature",
      #    "device": {
      #      "identifiers": [
      #         "pool_temperature_sensor"
      #      ],
      #      "name": "Pool Temperature",
      #      "model": "None",
      #      "manufacturer": "None"
      #    },
      #    "icon": "mdi:thermometer",
      #    "platform": "mqtt"
      #}
      #client.publish(topic=base_topic_cover + "config", payload=str(config_payload_cover), qos=0, retain=False)

      # Publish Temp
      client.publish(topic=base_topic_temp + "state", payload=str(temp), qos=0, retain=False)

      # Publish Cover
      #client.publish(topic=base_topic_cover + "state", payload=str(cover_state), qos=0, retain=False)

      time.sleep(6)
#******************************************

#-------------------------------------------------------------------------------------------------------
# main function
def main():
    client = mqtt.Client()
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.connect(mqtt_host, mqtt_port)
    client.loop_forever()

#---------------------------------------------------------------------------------------------------------------------------------
if __name__=="__main__":
    main()
#---------------------------------------------------------------------------------------------------------------------------------
