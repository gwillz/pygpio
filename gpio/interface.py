from abc import ABCMeta, abstractmethod
from avent import Avent

class GpioInterface(object, metaclass=ABCMeta):
    OUT = 0
    IN = 1
    OUT_PWM = 2
    DOWN = 4
    UP = 8
    
    def __init__(self, wrapper):
        self._wrapper = wrapper
    
    def _eventCallback(self, pin):
        self._wrapper.onEvent.fire(self._wrapper, pin)
    
    @abstractmethod
    def setup(self, pin, mode):
        pass
    
    @abstractmethod
    def write(self, pin, state):
        pass
    
    @abstractmethod
    def read(self, pin, state):
        pass
    
    @abstractmethod
    def writePwm(self, pin, state, freq=None):
        pass


## newfile --------------------------------


import RPi.GPIO as rpi

class RpiBackend(GpioInterface):
    MAP = {
        self.OUT: rpi.OUT,
        self.IN: rpi.IN,
        self.OUT_PWM: rpi.OUT,
        self.UP: rpi.UP,
        self.DOWN: rpi.DOWN
    }
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        
        self._pwms = {}
        rpi.setmode(rpi.BCM)
        rpi.setwarnings(False)
    
    def setup(self, pin, mode):
        rpi.setup(pin, self.MAP[mode])
        if mode == self.OUT_PWM:
            self._pwms[pin] = rpi.PWM(pin, self.PWM_FREQ)
    
    def write(self, pin, state):
        rpi.output(pin, self.MAP[state])
    
    def pwmWrite(self, pin, state, freq=None):
        if freq:
            self._pwms[pin].ChangeFrequency(freq)
        
        if state == self.DOWN:
            self._pwms[pin].stop()
        elif state == self.UP:
            self._pwms[pin].start(self.PWM_DUTY)
        


## newfile --------------------------------

class WiringBackend(GpioInterface):
    pass


class TestBackend(GpioInterface):
    pass

## newfile --------------------------------


class Pwm(object):
    def __init__(self, pin, backend):
        self._pin = pin
        self._backend = backend
    
    def start(self, freq=440):
        self._backend.pwmWrite(self._pin, GpioInterface.UP, freq)
    
    def stop(self):
        self._backend.pwmWrite(self._pin, GpioInterface.DOWN)
    
    def setFrequency(self, freq):
        self._backend.pwmWrite(self._pin, None, freq)


class Gpio(object):
    MODES = [GpioInterface.OUT, GpioInterface.IN, GpioInterface.OUT_PWM]
    STATES = [GpioInterface.UP, GpioInterface.DOWN]
    BACKENDS = ['RpiBackend', 'WiringBackend']
    
    PWM_FREQ = 100
    PWM_DUTY = 50
    
    def __init__(self, backend=None):
        self._backend = None
        self._pins = {}
        self.onInterrupt = Avent()
        
        if backend is None:
            for b in self.BACKENDS:
                try:
                    self._backend = globals()[b](self)
                    break
                except KeyError: pass
        
        elif not issubclass(backend, GpioInterface):
            raise RuntimeError('Invalid backend interface')
        else:
            self._backend = backend(self)
        
        if self._backend is None:
            raise RuntimeError('No backends available: {}'.format(self.BACKENDS))
    
    def setup(self, pin, mode):
        if mode not in self.MODES:
            raise TypeError("Invalid mode: {}".format(mode))
        if not isinstance(pin, list):
            pin = [pin]
        
        for p in pin:
            self._pins[p] = mode
            self._backend.setup(p, mode)
    
    def write(self, pin, state=MODES.UP):
        if pin not in self._pins:
            raise IndexError("Pin not configured")
        if state not in self.STATES:
            raise TypeError("Invalid state: {}".format(state))
        
        if self._pins[pin] == GpioInterface.OUT_PWM:
            return Pwm(self._backend, pin)
        
        self._backend.write(pin, state)
    
