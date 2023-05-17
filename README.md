# Pool

Controlling pool via Raspberry Pi, Python3, MQTT & HomeAssistant (auto-discovery)
## Requirements
* TBD
* HomeAssistant Instance with MQTT Mosquitto Broker
* Raspberry PI (I used rpi4)
* Wiring: TBD
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
        dtoverlay=w1-gpio,gpiopin=3
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
        #to see all possible args and the default values
        python3 pool/src/main.py -h 
        #Add args as needed
        #e.g. -mqttpw to add the password to access mqtt
        python3 pool/src/main.py -mqttpw TestPW
        ```
    * See /docs/raspberry-pi-pinout.jpeg to check the pinouts
    ![alt text](https://github.com/PhilippF1992/pool/blob/main/docs/raspberry-pi-pinout.jpeg?raw=true)

* Check HA if the "pool" device is now available withing Mosquitto-Broker
    ![alt text](https://github.com/PhilippF1992/pool/blob/main/docs/DeviceInHA.png?raw=true)
    ![alt text](https://github.com/PhilippF1992/pool/blob/main/docs/DeviceInHADetail.png?raw=true)

* Modify systemd service to match your args (line 14) 
    *   ```shell 
        nano /home/pi/pool/service/python_pool.service
        ```
* Make add service to systemd 
    *   ```shell 
        sudo cp /home/pi/pool/service/python_pool.service /etc/systemd/system/python_pool.service 
        ```
* Enable service to run at boot
    *   ```shell 
        systemctl enable python_pool.service
        ```
* Restart RPI to run service
    *   ```shell
        sudo reboot
        ```

* Check if everything started properly
    * Login via ssh
    *   ```shell
        systemctl status --user python_pool.service
        ```
    