import time
from .device import *
from .switches.gpio_switch import *
import paho.mqtt.client as mqtt

class Pump:
    def __init__(self, uniq_id, device: Device, client: mqtt.Client, gpio_pump_level_1, gpio_pump_level_2, gpio_pump_level_3, gpio_pump_level_stop, connect_on):
        self.uniq_id = uniq_id
        self.pump_level_1 = GPIO_Switch("Pump Level 1", "pool_level_1", device, client, gpio_pump_level_1, connect_on, uniq_id)
        self.pump_level_2 = GPIO_Switch("Pump Level 2", "pool_level_2", device, client, gpio_pump_level_2, connect_on, uniq_id)
        self.pump_level_3 = GPIO_Switch("Pump Level 3", "pool_level_3", device, client, gpio_pump_level_3, connect_on, uniq_id)
        self.pump_level_stop = GPIO_Switch("Pump Level Stop", "pool_level_stop", device, client, gpio_pump_level_stop, connect_on, uniq_id)
        self.pump_level_1.set_on()
        self.pump_level_2.set_off()
        self.pump_level_3.set_off()
        self.pump_level_stop.set_off()

    def subscribe(self):
        self.pump_level_1.subscribe()
        self.pump_level_2.subscribe()
        self.pump_level_3.subscribe()
        self.pump_level_stop.subscribe()

    def on_message(self, message):
        payload=str(message.payload.decode("utf-8"))
        if (self.pump_level_1.uniq_id in message.topic):
            if (payload=="True"):
                self.pump_level_2.set_off()
                self.pump_level_3.set_off()
                self.pump_level_stop.set_off()
                time.sleep(0.5)
                self.pump_level_1.set_on()
            else:
                self.pump_level_1.set_off()
        if (self.pump_level_2.uniq_id in message.topic):
            if (payload=="True"):
                self.pump_level_1.set_off()
                self.pump_level_3.set_off()
                self.pump_level_stop.set_off()
                time.sleep(0.5)
                self.pump_level_2.set_on()
            else:
                self.pump_level_2.set_off()
        if (self.pump_level_3.uniq_id in message.topic):
            if (payload=="True"):
                self.pump_level_1.set_off()
                self.pump_level_2.set_off()
                self.pump_level_stop.set_off()
                time.sleep(0.5)
                self.pump_level_3.set_on()
            else:
                self.pump_level_3.set_off
        if (self.pump_level_stop.uniq_id in message.topic):
            if (payload=="True"):
                self.pump_level_1.set_off()
                self.pump_level_2.set_off()
                self.pump_level_3.set_off()
                time.sleep(0.5)
                self.pump_level_stop.set_on()
            else:
                self.pump_level_stop.set_off()