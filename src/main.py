import time
import argparse
import systemd.daemon
import paho.mqtt.client as mqtt
from classes.device import *
from classes.cover import *
from classes.pump import *
from classes.light import *
from classes.sensors.ds18b20 import *

parser = argparse.ArgumentParser(description='Controll your Pool via MQTT and HA')
parser.add_argument('-gcc', dest='gpio_cover_closed', type=int, default=11,
                    help="GPIO pin Cover Closed(Default: 11)")
parser.add_argument('-gco', dest='gpio_cover_opened', type=int, default=9,
                    help="GPIO pin Cover Opened(Default: 9)")
parser.add_argument('-gccg', dest='gpio_cover_closing', type=int, default=10,
                    help="GPIO pin Cover Closing(Default: 10)")
parser.add_argument('-gcog', dest='gpio_cover_opening', type=int, default=22,
                    help="GPIO pin Cover Opening(Default: 22)")
parser.add_argument('-gci', dest='gpio_cover_impuls', type=int, default=5,
                    help="GPIO pin Cover Impuls(Default: 5)")
parser.add_argument('-mqttuser', dest='mqtt_user', type=str, default="mqtt",
                    help="MQTT Username (Default: mqtt)")
parser.add_argument('-mqttpw', dest='mqtt_password', type=str, default="",
                    help="MQTT Password (Default: no pw)")
parser.add_argument('-mqtthost', dest='mqtt_host', type=str, default="homeassistant.local",
                    help="MQTT Host (Default: homeassistant.local)")
parser.add_argument('-mqttport', dest='mqtt_port', type=int, default=1883,
                    help="MQTT Port (Default: 1883)")
parser.add_argument('-connect_on', dest='connect_on', type=any, default=GPIO.LOW,
                    help="Connect on (Default: GPIO.HIGH)")
parser.add_argument('-gpl1', dest='gpio_pump_level_1', type=int, default=6,
                    help="GPIO Pump Level 1(Default: 6)")
parser.add_argument('-gpl2', dest='gpio_pump_level_2', type=int, default=13,
                    help="GPIO Pump Level 2(Default: 13)")
parser.add_argument('-gpl3', dest='gpio_pump_level_3', type=int, default=19,
                    help="GPIO Pump Level 3(Default: 19)")
parser.add_argument('-gplstop', dest='gpio_pump_level_stop', type=int, default=26,
                    help="GPIO Pump Level Stop(Default: 26)")
parser.add_argument('-lightip', dest='light_ip', type=str, default="199.2.22.59",
                    help="Brio WIL Light IP(Default: 199.2.22.59)")
parser.add_argument('-lightport', dest='light_port', type=int, default=30302,
                    help="Brio WIL Light Port(Default: 30302)")
args = parser.parse_args()

GPIO.setmode (GPIO.BCM)
GPIO.setwarnings(False)


client = mqtt.Client()
client.username_pw_set(args.mqtt_user, args.mqtt_password)

device = Device(["pool"], "pool", "v1", "rpi", "me")
ds18b20 = DS18B20("Pool Temperature", "pool_temperature", device, client)
cover = Cover("cover", device, client, args.gpio_cover_closed, args.gpio_cover_opened, args.gpio_cover_closing, args.gpio_cover_opening, args.gpio_cover_impuls, args.connect_on)
pump = Pump("pump", device, client, args.gpio_pump_level_1, args.gpio_pump_level_2, args.gpio_pump_level_3, args.gpio_pump_level_stop, args.connect_on)
light = Light("light", device, client, args.light_ip, args.light_port)
connected = False
def on_message(client, userdata, message):
    if (cover.uniq_id in message.topic):
        cover.on_message(message)
    if (pump.uniq_id in message.topic):
        pump.on_message(message)
    if (light.uniq_id in message.topic):
        light.on_message(message)

def on_connect(client, userdata, flags, rc):
    cover.subscribe()
    pump.subscribe()
    light.subscribe()
    cover.send_config()
    pump.send_config()
    light.send_config()
    connected = True

def on_disconnect(client, userdata, rc):
    connected = False

def on_log(client, userdata, paho_log_level, message):
    print(message)

#client.on_log = on_log
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(args.mqtt_host, args.mqtt_port)
client.loop_start()
systemd.daemon.notify('READY=1')
while True:
    ds18b20.send_data()
    cover.send_data()
    time.sleep(2)




