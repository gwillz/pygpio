#!/usr/bin/bash

# get librpip - this initializes the pwm clock and sets the correct permissions
wget http://librpip.frasersdev.net/wp-content/uploads/2016/03/librpip-0.3.2.tar.gz
tar -xf librpip-0.3.2.tar.gz
cd librpip-0.3.2/

# install librpip
./configure
make
sudo make install

# install pwm init service
cp distro/arch/pwm-init.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable pwm-init

# create pwm group
sudo groupadd -R pwm
sudo usermod -aG pwm pi

# add pwm to the boot config
sudo su -c 'echo dtoverlay=pwm,pin=12,func=4 > /boot/config.txt'
