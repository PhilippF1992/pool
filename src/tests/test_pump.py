import RPi.GPIO as GPIO
import time
import sys

if (len(sys.argv) < 9):
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
GPIO.output(pump_one, GPIO.LOW)
GPIO.output(pump_two, GPIO.LOW)
GPIO.output(pump_three, GPIO.LOW)
GPIO.output(pump_stop, GPIO.LOW)

while True:
    if int(sys.args[5]) == 1: 
        GPIO.output(pump_two, GPIO.LOW)
        GPIO.output(pump_three, GPIO.LOW)
        GPIO.output(pump_stop, GPIO.LOW)
        GPIO.output(pump_one, GPIO.HIGH)
    if int(sys.args[5]) == 2: 
        GPIO.output(pump_one, GPIO.LOW)
        GPIO.output(pump_three, GPIO.LOW)
        GPIO.output(pump_stop, GPIO.LOW)
        GPIO.output(pump_two, GPIO.HIGH)
    if int(sys.args[5]) == 3: 
        GPIO.output(pump_two, GPIO.LOW)
        GPIO.output(pump_one, GPIO.LOW)
        GPIO.output(pump_stop, GPIO.LOW)
        GPIO.output(pump_three, GPIO.HIGH)
    if int(sys.args[5]) == 0: 
        GPIO.output(pump_two, GPIO.LOW)
        GPIO.output(pump_three, GPIO.LOW)
        GPIO.output(pump_one, GPIO.LOW)
        GPIO.output(pump_stop, GPIO.HIGH)