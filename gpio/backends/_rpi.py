import RPi.GPIO as rpi
from gpio.interface import GpioInterface
from gpio import modes

class RpiBackend(GpioInterface):
    MAP = {
        modes.OUT: rpi.OUT,
        modes.IN: rpi.IN,
        modes.PWM: rpi.OUT,
        modes.UP: rpi.UP,
        modes.DOWN: rpi.DOWN
    }
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        
        self._pwms = {}
        rpi.setmode(rpi.BCM)
        rpi.setwarnings(False)
    
    def setup(self, pin, mode):
        rpi.setup(pin, self.MAP[mode])
        if mode == modes.PWM:
            self._pwms[pin] = rpi.PWM(pin, self._wrapper.PWM_FREQ)
    
    def write(self, pin, state):
        rpi.output(pin, self.MAP[state])
    
    def pwmWrite(self, pin, state, freq=None):
        if freq:
            self._pwms[pin].ChangeFrequency(freq)
        
        if state == modes.DOWN:
            self._pwms[pin].stop()
        elif state == modes.UP:
            self._pwms[pin].start(self._wrapper.PWM_DUTY)
        
