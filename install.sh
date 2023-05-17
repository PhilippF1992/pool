#!/bin/bash

sudo apt update
sudo apt upgrade -y
sudo apt install git -y
sudo apt-get install python3-rpi.gpio
sudo apt-get install python3-pip
sudo pip3 install paho-mqtt

sudo useradd -r -s /bin/false python_pool

sudo bash -c "echo 'dtoverlay=w1-gpio,gpiopin=17' >> /boot/config.txt"

git clone https://github.com/PhilippF1992/pool.git

sudo cp -r pool /usr/local/lib/

sudo chown root:root /usr/local/lib/pool/

sudo chmod 644 /usr/local/lib/pool/

sudo cp /usr/local/lib/pool/service/python_pool.service /etc/systemd/system/python_pool.service 

sudo systemctl enable python_pool.service

nano /etc/systemd/system/python_pool.service 