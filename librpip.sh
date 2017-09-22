#!/bin/bash

# create pwm group
sudo groupadd -r pwm
sudo usermod -aG pwm pi

# get librpip - this initializes the pwm clock and sets the correct permissions
if [[ ! -d "librpip-0.3.2" ]]; then
  wget http://librpip.frasersdev.net/wp-content/uploads/2016/03/librpip-0.3.2.tar.gz
  tar -xf librpip-0.3.2.tar.gz
fi
cd librpip-0.3.2/

# build
if [[ ! -e "./bin/pwmclk" ]]; then
  ./configure
  make
fi

# install
[[ -d "/usr/local/bin/librpip-util" ]] || sudo make install

# install pwm init service
sudo cp distro/arch/pwm-init.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable pwm-init

# add pwm to the boot config
echo ""
echo "add this to your /boot/config.txt"
echo "##"
echo "dtoverlay=pwm,pin=12,func=4"
echo "##"
