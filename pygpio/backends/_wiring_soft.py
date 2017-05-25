# import os
import wiringpi as wpi # pylint: disable=import-error
from pygpio.interface import GpioInterface
from pygpio import modes

# pragma pylint: disable=protected-access

class WiringBackend(GpioInterface):
    MAP = {
        modes.OUT: wpi.OUTPUT,
        modes.IN: wpi.INPUT,
        modes.RISING: wpi.INPUT,
        modes.FALLING: wpi.INPUT,
        modes.PWM: wpi.OUTPUT,
        True: wpi.HIGH,
        False: wpi.LOW
    }
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        self._pwmfreq = wrapper.PWM_FREQ
        
        # os.popen('gpio export 18 out')
        wpi.wiringPiSetupSys() # no sudo
    
    def setup(self, pin, mode):
        if mode == modes.PWM:
            wpi.softToneCreate(pin)
        
        return True
    
    def clear(self, pin):
        mode = self._wrapper._pins[pin]
        if mode == modes.PWM:
            wpi.softTimeWrite(pin, 0)
        else:
            wpi.digitalWrite(pin, wpi.LOW)
    
    def write(self, pin, state):
        wpi.digitalWrite(pin, self.MAP[state])
    
    def read(self, pin):
        return wpi.digitalRead(pin)
    
    def writePwm(self, pin, state, freq=None, duty=None):
        # TODO duty
        if freq:
            self._pwmfreq = freq
        if state:
            wpi.softToneWrite(pin, self._pwmfreq)
        elif state is False:
            wpi.softToneWrite(pin, 0)
