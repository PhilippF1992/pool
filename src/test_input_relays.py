import RPi.GPIO as GPIO
import time
# logical pins
closed_relay_pin = 5
opened_relay_pin = 6
closing_relay_pin = 13
opening_relay_pin = 26

GPIO.setmode (GPIO.BCM)
GPIO.setup(closed_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opened_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(closing_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opening_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(closed_relay_pin) == GPIO.HIGH:
        print("closed_relay_pin was powered!")
    if GPIO.input(opened_relay_pin) == GPIO.HIGH:
        print("closed_relay_pin was powered!")
    if GPIO.input(closing_relay_pin) == GPIO.HIGH:
        print("closed_relay_pin was powered!")
    if GPIO.input(opening_relay_pin) == GPIO.HIGH:
        print("closed_relay_pin was powered!")