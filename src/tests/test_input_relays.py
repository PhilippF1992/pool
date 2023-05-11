import RPi.GPIO as GPIO
import time
import sys

if (len(sys.argv) < 9):
   raise  ValueError('Input arguments of pins not provided')

# logical pins
closed_relay_pin = int(sys.argv[1])
opened_relay_pin = int(sys.argv[2])
closing_relay_pin = int(sys.argv[3])
opening_relay_pin = int(sys.argv[4])

GPIO.setmode (GPIO.BCM)
GPIO.setup(closed_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opened_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(closing_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(opening_relay_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    if GPIO.input(closed_relay_pin) == GPIO.HIGH:
        print("closed_relay_pin was powered!")
    if GPIO.input(opened_relay_pin) == GPIO.HIGH:
        print("opened_relay_pin was powered!")
    if GPIO.input(closing_relay_pin) == GPIO.HIGH:
        print("closing_relay_pin was powered!")
    if GPIO.input(opening_relay_pin) == GPIO.HIGH:
        print("opening_relay_pin was powered!")