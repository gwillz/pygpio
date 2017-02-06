import RPi.GPIO as rpi
from gpio.interface import GpioInterface
from gpio import modes

class RpiBackend(GpioInterface):
    MAP = {
        modes.OUT: rpi.OUT,
        modes.IN: rpi.IN,
        modes.PWM: rpi.OUT,
        True: rpi.HIGH,
        False: rpi.LOW
    }
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        
        self._pwms = {}
        rpi.setmode(rpi.BCM)
        rpi.setwarnings(False)
    
    def setup(self, pin, mode):
        rpi.setup(pin, self.MAP[mode])
        if mode == modes.PWM:
            self._pwms[pin] = rpi.PWM(pin, self._wrapper)
        elif mode == modes.IN:
            rpi.add_event_detect(pin, rpi.RISING, self._eventCallback, 50)
    
    def write(self, pin, state):
        rpi.output(pin, self.MAP[state])
    
    def read(self, pin):
        return rpi.input(pin) == 0
    
    def writePwm(self, pin, state, freq=None):
        if freq:
            self._pwms[pin].ChangeFrequency(freq)
        
        if state:
            self._pwms[pin].start(self._wrapper.PWM_DUTY*100)
        elif state is False:
            self._pwms[pin].stop()
    
