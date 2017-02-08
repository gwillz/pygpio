import RPi.GPIO as rpi
from pygpio.interface import GpioInterface
from pygpio import modes

class RpiBackend(GpioInterface):
    MAP = {
        modes.OUT: rpi.OUT,
        modes.IN: rpi.IN, # and BOTH
        modes.RISING: rpi.IN,
        modes.FALLING: rpi.IN,
        modes.PWM: rpi.OUT,
        True: rpi.HIGH,
        False: rpi.LOW
    }
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        
        self._pwms = {} #: pin: GPIO.PWM()
        self._pwmduty = self._wrapper.PWM_DUTY
        
        rpi.setmode(rpi.BCM)
        rpi.setwarnings(False)
    
    def setup(self, pin, mode):
        rpi.setup(pin, self.MAP[mode])
        if mode == modes.PWM:
            self._pwms[pin] = rpi.PWM(pin, self._wrapper.PWM_FREQ)
        elif mode & modes._RISING:
            rpi.add_event_detect(pin, rpi.RISING, self._risingCallback, 100)
        elif mode & modes._FALLING:
            rpi.add_event_detect(pin, rpi.FALLING, self._fallingCallback, 100)
        
        return True
    
    def clear(self, pin):
        mode = self._wrapper._pins[pin]
        if mode == modes.PWM:
            self._pwms[pin].stop()
            del self._pwms[pin]
        
        rpi.cleanup(pin)
    
    def write(self, pin, state):
        rpi.output(pin, self.MAP[state])
    
    def read(self, pin):
        return rpi.input(pin) == 0
    
    def writePwm(self, pin, state, freq=None, duty=None):
        if freq: self._pwms[pin].ChangeFrequency(freq)
        if duty: self._pwmduty = duty
        
        if state:
            self._pwms[pin].start(self._pwmduty*100)
        elif state is False:
            self._pwms[pin].stop()
    
    def _risingCallback(self, pin):
        self._wrapper.onRising.fire(self._wrapper, pin)
        
    def _fallingCallback(self, pin):
        self._wrapper.onFalling.fire(self._wrapper, pin)
    
