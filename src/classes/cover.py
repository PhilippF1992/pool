import paho.mqtt.client as mqtt
from device import *
from binary_sensors.normal import *
from switches.auto_off import *

class Cover:
    def __init__(self, uniq_id, device: Device, client: mqtt.Client, gpio_cover_closed, gpio_cover_opened, gpio_cover_closing, gpio_cover_opening, gpio_cover_impuls, connect_on):
        self.uniq_id = uniq_id
        self.cover_closed = Binary("Pool Cover Closed", "pool_cover_closed", device, client, gpio_cover_closed, uniq_id)
        self.cover_opened = Binary("Pool Cover Opened", "pool_cover_opened", device, client, gpio_cover_opened, uniq_id)
        self.cover_closing = Binary("Pool Cover Closing", "pool_cover_closing", device, client, gpio_cover_closing, uniq_id)
        self.cover_opening = Binary("Pool Cover Opening", "pool_cover_opening", device, client, gpio_cover_opening, uniq_id)
        self.cover_impuls = AutoOff("Pool Cover Impuls", "pool_cover_impuls", device, client, gpio_cover_impuls, connect_on, uniq_id)
    
    def send_data(self):
        self.cover_closed.send_data
        self.cover_opened.send_data
        self.cover_closing.send_data
        self.cover_opening.send_data

    def on_message(self, message):
        self.cover_impuls(message)