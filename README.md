# Pool

Controlling your pool via Raspberry Pi, Python3, MQTT & HomeAssistant (auto-discovery)
## Requirements
* Controlled Units
    * Speck Badu Alpha Eco Soft https://www.speck-pumps.com/de/p/badu-alpha-eco-soft/?a=badu&v=3a52f3c22ed6
    * T&A Aquatop Poolcover https://www.t-and-a.be/en/products/aquatop/drive
* HomeAssistant Instance with MQTT Mosquitto Broker
* Raspberry PI (I used rpi4)
* Wiring:
    * Relay Hat for RPI https://www.amazon.de/gp/product/B083GNQ7RN/
    * DS18B20 waterproof thermometer https://www.amazon.de/dp/B074XH3L71
    * 1 270 Ohm Resistor
    * 1 4,7k Ohm Resistor
    * 8 ScrewTerminals 
## Setup:
* Create sd-card via Imager https://www.raspberrypi.com/software/
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
        sudo apt-get install python3-rpi.gpio -y
        sudo apt-get install python3-pip -y
        sudo apt install python3-systemd -y 
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

        The linked RPI Hat uses GPIO 5 (AquaTop Impuls),6 (Pump L1),13 (Pump L2),19 (Pump L3),26 (Pump Stop) and 12(unused Relay) by default
        I used GPIO 3 for the DS18B20 and GPIO 22,10,9 and 11 for the relays of the AquaTop.

        ![alt text](https://github.com/PhilippF1992/pool/blob/main/docs/raspberry-pi-pinout.jpeg?raw=true)

* Check HA if the "pool" device is now available withing Mosquitto-Broker
    ![alt text](https://github.com/PhilippF1992/pool/blob/main/docs/DeviceInHA.png?raw=true)
    ![alt text](https://github.com/PhilippF1992/pool/blob/main/docs/DeviceInHADetail.png?raw=true)

* Modify systemd service to match your args (line 14) 
    *   ```shell 
        nano pool/service/python_pool.service
        ```
* Create User mentioned in service and add it to the gpio group
    *   ```shell 
        sudo useradd -r -s /bin/false python_pool
        sudo adduser python_pool gpio
        ```
* Copy files to /usr/local/lib
    *   ```shell 
        sudo cp -r pool /usr/local/lib/

        sudo chown root:root /usr/local/lib/pool/src/main.py

        sudo chmod 644 /usr/local/lib/pool/src/main.py
        ```
* Add service to systemd 
    *   ```shell 
        sudo cp /usr/local/lib/pool/service/python_pool.service /etc/systemd/system/python_pool.service 
        ```
* Enable service to run at boot
    *   ```shell 
        sudo systemctl enable systemd-networkd.service systemd-networkd-wait-online.service
        sudo systemctl enable python_pool.service
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
    *   ```shell
        journalctl --unit python_pool -f        
        ```
    