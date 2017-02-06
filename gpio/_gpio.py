from avent import Avent
from gpio.interface import GpioInterface
from gpio.backends._native import NativeBackend
from gpio._pwm import Pwm
from gpio import modes, notes as note

class Gpio(object):
    MODES = [modes.OUT, modes.IN, modes.PWM]
    
    PWM_FREQ = note.A
    PWM_DUTY = 0.50
    
    def __init__(self, backend=None):
        self._backend = None
        self._pins = {}
        self.onEvent = Avent()
        
        if backend is None:
            backend = NativeBackend
        if not issubclass(backend, GpioInterface):
            raise RuntimeError('Invalid backend interface')
        
        self._backend = backend(self)
    
    def setup(self, pin, mode):
        if mode not in self.MODES:
            raise TypeError("Invalid mode: {}".format(mode))
        
        if mode == modes.PWM and isinstance(pin, int):
            return Pwm(self._backend, pin)
        
        if isinstance(pin, int):
            pin = [pin]
        
        for p in pin:
            self._pins[p] = mode
            self._backend.setup(p, mode)
    
    def write(self, pin, state=True):
        if pin not in self._pins:
            raise IndexError("Pin not configured")
        
        mode = self._pins[pin]
        
        if mode == modes.PWM:
            return Pwm(self._backend, pin)
        
        elif mode != modes.OUT:
            raise TypeError("pin {} not configured for output".format(pin))
        
        self._backend.write(pin, state)
    
    def read(self, pin):
        if pin not in self._pins:
            raise IndexError("Pin not configured")
        if self._pins[pin] != modes.IN:
            raise TypeError("pin {} not configured for input".format(pin))
        
        return self._backend.read(pin)
    
