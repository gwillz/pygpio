from gpio.interface import GpioInterface
from gpio import modes

class Pwm(object):
    def __init__(self, pin, backend):
        self._pin = pin
        self._backend = backend
    
    def start(self, freq=440):
        self._backend.pwmWrite(self._pin, modes.UP, freq)
    
    def stop(self):
        self._backend.pwmWrite(self._pin, modes.DOWN)
    
    def setFrequency(self, freq):
        self._backend.pwmWrite(self._pin, None, freq)
