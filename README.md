# Pool

Controlling pool via Raspberry pi 4 & Home Assistant
## Requirements
* Raspberry Pi 4
* DS18B20 Thermometer 
* AquaTop Poolcover
* 
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
* Install git
    *   ```shell 
        sudo apt install git -y 
        ```
* Install python libraries
    *   ```shell 
        sudo apt-get install python3-rpi.gpio
        ```
* Clone git repo
    *   ```shell 
        git clone https://github.com/PhilippF1992/pool.git
        ```
* Run Tests 
    *  Enter directory
        ```shell 
        cd pool/src
        ```

        *   Input relays:
            ```shell 
            python3 test_input_relays.py 
            ```