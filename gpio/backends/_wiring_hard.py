# import os
import wiringpi as wpi
from gpio.interface import GpioInterface
from gpio import modes

class WiringHardBackend(GpioInterface):
    MAP = {
        modes.OUT: wpi.OUTPUT,
        modes.IN: wpi.INPUT,
        modes.PWM: wpi.PWM_OUTPUT,
        True: wpi.HIGH,
        False: wpi.LOW
    }
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        
        wpi.wiringPiSetupGpio() # requires sudo
    
    def setup(self, pin, mode):
        wpi.pinMode(self.MAP[mode])
        if mode == modes.PWM:
            wpi.pwmSetMode(wpi.PWM_MODE_MS)
            wpi.pwmSetClock(int(19200000*self._wrapper.PWM_FREQ)//2)
            wpi.pwmSetRange(int(19200000*self._wrapper.PWM_FREQ))
    
    def write(self, pin, state):
        wpi.digitalWrite(pin, self.MAP[state])
    
    def read(self, pin):
        return wpi.digitalRead(pin)
    
    def writePwm(self, pin, state, freq=None):
        print('WIP: wiringPi hardware PWM')
        if freq:
            wpi.pwmSetClock(int(19200000*freq)//2)
            wpi.pwmSetRange(int(19200000*freq))
        
        if state:
            wpi.pwmWrite(pin, int(self._wrapper.PWM_DUTY*4096))
        elif state is False:
            wpi.pwmWrite(pin, 0)
