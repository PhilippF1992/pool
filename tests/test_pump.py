import RPi.GPIO as GPIO
import time
import sys

if (len(sys.argv) < 5):
   raise  ValueError('Input arguments of pins not provided')

# logical pins
pump_one = int(sys.argv[1])
pump_two = int(sys.argv[2])
pump_three = int(sys.argv[3])
pump_stop = int(sys.argv[4])

GPIO.setmode (GPIO.BCM)
GPIO.setup(pump_one, GPIO.OUT)
GPIO.setup(pump_two, GPIO.OUT)
GPIO.setup(pump_three, GPIO.OUT)
GPIO.setup(pump_stop, GPIO.OUT)
GPIO.output(pump_one, GPIO.HIGH)
GPIO.output(pump_two, GPIO.HIGH)
GPIO.output(pump_three, GPIO.HIGH)
GPIO.output(pump_stop, GPIO.HIGH)

while True:
    if int(sys.argv[5]) == 1: 
        GPIO.output(pump_two, GPIO.HIGH)
        GPIO.output(pump_three, GPIO.HIGH)
        GPIO.output(pump_stop, GPIO.HIGH)
        GPIO.output(pump_one, GPIO.LOW)
    if int(sys.argv[5]) == 2: 
        GPIO.output(pump_one, GPIO.HIGH)
        GPIO.output(pump_three, GPIO.HIGH)
        GPIO.output(pump_stop, GPIO.HIGH)
        GPIO.output(pump_two, GPIO.LOW)
    if int(sys.argv[5]) == 3: 
        GPIO.output(pump_two, GPIO.HIGH)
        GPIO.output(pump_one, GPIO.HIGH)
        GPIO.output(pump_stop, GPIO.HIGH)
        GPIO.output(pump_three, GPIO.LOW)
    if int(sys.argv[5]) == 0: 
        GPIO.output(pump_two, GPIO.HIGH)
        GPIO.output(pump_three, GPIO.HIGH)
        GPIO.output(pump_one, GPIO.HIGH)
        GPIO.output(pump_stop, GPIO.LOW)