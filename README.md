# Pool

Controlling pool via Raspberry pi 4 & Home Assistant
## Requirements
* Raspberry Pi 4
* DS18B20 Thermometer 
* AquaTop Poolcover
* 4 resistors around 250 Ohm
* 1 resistor 4,7k Ohm
## Setup:
* Create sd-card via Imager: https://www.raspberrypi.com/software/
    * Lite OS 64-bit
    * Set Wifi and enable ssh 
* Start up rpi4
* Login via ssh
* Update repositories
    *   ```shell 
        sudo apt update 
        ```
    *   ```shell 
        sudo apt upgrade -y 
        ```
* Enable GPIO for BS18B20: https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
(modprobe not needed)
    *   ```shell
        sudo nano /boot/config.txt
        ```
    * add to the bottom of the file:
        ```shell
        dtoverlay=w1-gpio,gpiopin=17
        ```
    * reboot
        ```shell
        sudo reboot
        ```
    * check (when connected)
        ```shell
        lsmod | grep w1
        
        w1_therm               28672  0
        w1_gpio                16384  0
        wire                   49152  2 w1_gpio,w1_therm
        ```

* Install git
    *   ```shell 
        sudo apt install git -y 
        ```
* Install python libraries
    *   ```shell 
        sudo apt-get install python3-rpi.gpio
        sudo apt-get install python3-pip
        sudo pip3 install paho-mqtt
        sudo pip3 install rpi-rf
        ```
* Clone git repo
    *   ```shell 
        git clone https://github.com/PhilippF1992/pool.git
        ```
* Run Tests 
    *  Enter directory
        ```shell 
        cd pool
        ```
        *   Input relays:
            ```shell 
            python3 src/tests/test_input_relays.py 5 6 13 26
            ```
        *   Input Temp:
            ```shell 
            python3 src/tests/test_thermometer.py 
            ```