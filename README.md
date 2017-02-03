PyGPIO
======
This project attempts to unify the many different ways to interface with GPIO
in a unified, formal, and consistent manner. It provides an simple interface for
controlling digital output and PWM, and an event library for interrupt inputs.

Hopefully, through this library your projects can make use of whichever backend
suits your needs without having to commit. Using this interface library also
allows for easier unit-testing with a mock backend.

Requirements and Supported Backends
-----------------------------------
 + [Avent](https://git.gwillz.com.au/mk2/avent) >= 0.6
 + RPi.GPIO >= 6.?
 + WiringPi >= 2.?


Authors
-------
 + [Gwilyn Saunders](https://git.gwillz.com.au/u/gwillz)
 + [MK2 Engineering Solutions](https://mk2es.com.au)
