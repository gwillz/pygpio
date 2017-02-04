# import os
import wiringpi as wpi
from gpio.interface import GpioInterface
from gpio import modes

class WiringBackend(GpioInterface):
    MAP = {
        modes.OUT: wpi.OUTPUT,
        modes.IN: wpi.INPUT,
        modes.PWM: wpi.OUTPUT,
        True: wpi.HIGH,
        False: wpi.LOW
    }
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        self._pwmfreq = 440
        
        # os.popen('gpio export 18 out')
        wpi.wiringPiSetupSys()
    
    def setup(self, pin, mode):
        if mode == modes.PWM:
            wpi.softToneCreate(pin)
        
    def write(self, pin, state):
        wpi.digitalWrite(pin, self.MAP[state])
    
    def read(self, pin):
        wpi.digitalRead(pin)
    
    def writePwm(self, pin, state, freq=None):
        if freq:
            self._pwmfreq = freq
        
        if state:
            wpi.softToneWrite(pin, self._pwmfreq)
        elif state is False:
            wpi.softToneWrite(pin, 0)
