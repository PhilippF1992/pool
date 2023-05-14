# Pool

Controlling pool via Raspberry pi 4 & Home Assistant
## Requirements
* TBD
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
* Enable GPIO for DS18B20: 
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
    * check (probe needs to be connected)
        ```shell
        lsmod | grep w1
        
        #w1_therm               28672  0
        #w1_gpio                16384  0
        #wire                   49152  2 w1_gpio,w1_therm
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
        ```
* Clone git repo
    *   ```shell 
        git clone https://github.com/PhilippF1992/pool.git
        ```

* Run code manually
    *   ```shell 
        #Add args as needed
        #e.g. -mqttpw to add the password to access mqtt
        python3 pool/src/main.py 
        ```

* Modify systemd service to match your args (line 14) 
    *   ```shell 
        nano /home/pi/pool/service/python_pool.service
        ```
* Make sure user systemd config is in place and add service
    *   ```shell 
        mkdir -p /home/pi/.config/systemd/user
        cp /home/pi/pool/service/python_pool.service 
        ```
* Enable service to run at boot
    *   ```shell 
        systemctl --user enable python_pool.service
        ```
