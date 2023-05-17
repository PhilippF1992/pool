#!/bin/bash

sudo apt update
sudo apt upgrade -y
sudo apt install git -y
sudo apt install python3-rpi.gpio -y
sudo apt install python3-pip -y
sudo apt install python3-systemd -y 
sudo pip3 install paho-mqtt

sudo useradd -r -s /bin/false python_pool

sudo adduser python_pool gpio

sudo bash -c "echo 'dtoverlay=w1-gpio,gpiopin=3' >> /boot/config.txt"

git clone https://github.com/PhilippF1992/pool.git

sudo cp -r pool /usr/local/lib/

sudo chown root:root /usr/local/lib/pool/src/main.py

sudo chmod 644 /usr/local/lib/pool/src/main.py

sudo cp /usr/local/lib/pool/service/python_pool.service /etc/systemd/system/python_pool.service 

sudo systemctl enable python_pool.service

sudo nano /etc/systemd/system/python_pool.service 