PyGPIO
======

![build status](https://git.mk2es.com.au/gwillz/pygpio/badges/master/build.svg)
![coverage report](https://git.mk2es.com.au/gwillz/pygpio/badges/master/coverage.svg)

This project attempts to unify the many different ways to interface with GPIO
in a unified, formal, and consistent manner. It provides an simple interface for
controlling digital output and PWM, and an event library for interrupt inputs.

Hopefully, through this library your projects can make use of whichever backend
suits your needs without having to commit to one form or another. Using this
interface library also allows for easier unit-testing with a mock backend.


Supported Backends
-----------------------------------
 + RPi.GPIO >= 0.6+
 + WiringPi >= 2.0+
 + PyGPIO Native


Usage
-----
```python
from pygpio import Gpio, modes

# default uses NativeBackend
g = Gpio() # or Gpio(WiringBackend), Gpio(RpiBackend)

# output, numbering in BCM/GPIO
g.setup(23, modes.OUT)
g.write(23, True) # turn on
g.write(23, False) # turn off

# input
g.setup(24, modes.IN)
print(g.read(24))

# interrupt events
def callme(sender, pin):
    print("event on", pin)
g.onFalling += callme
g.onRising += callme

 # PWM setup returns a Pwm() object
p = g.setup(18, modes.PWM)
p.start(440, duty=0.50)
p.stop()

# pygpio includes a notes library for creating music
from pygpio import notes
p.start(notes.Gs * notes.octave.up)

# also a 'music score' format
p.playScore([0.1, notes.A, notes.C, note.E])
p.playScore(notes.scores.birthday)

g.cleanup() # this is also called when python exits (via atexit)
```


Setup for Native Backend
------------------------
```sh
# get librpip - this initializes the pwm clock and sets the correct permissions
wget http://librpip.frasersdev.net/wp-content/uploads/2016/03/librpip-0.3.2.tar.gz
tar -xf librpip-0.3.2.tar.gz
cd librpip-0.3.2/

# create pwm group
sudo groupadd -r pwm
sudo usermod -aG pwm pi

# install librpip
./configure
make
sudo make install

# install pwm init service
sudo cp distro/arch/pwm-init.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable pwm-init

# add pwm to the boot config
sudo su -c 'echo dtoverlay=pwm,pin=12,func=4 > /boot/config.txt'

sudo reboot
```


Pin Channel Mapping
-------------------

(for Raspberry Pi)

*Note: pins >40 are only available on the Compute Module*


| PWM  | Pin | func | mode |
|------|-----|------|------|
| PWM0 | 12  | 4    | alt0 |
| PWM0 | 18  | 2    | alt5 |
| PWM0 | 40  | 4    | alt0 |
| PWM0 | 52  | 5    | alt1 |
| PWM1 | 13  | 4    | alt0 |
| PWM1 | 19  | 2    | alt5 |
| PWM1 | 41  | 4    | alt0 |
| PWM1 | 45  | 4    | alt0 |
| PWM1 | 53  | 5    | alt1 |

