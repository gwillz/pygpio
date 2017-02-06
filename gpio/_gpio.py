from avent import Avent
from gpio.interface import GpioInterface
from gpio._pwm import Pwm
from gpio import modes

BULTIN_BACKENDS = ['RpiBackend', 'WiringBackend']

class Gpio(object):
    MODES = [modes.OUT, modes.IN, modes.PWM]
    
    PWM_FREQ = 100
    PWM_DUTY = 50
    
    def __init__(self, backend=None):
        self._backend = None
        self._pins = {}
        self.onEvent = Avent()
        
        if backend is None:
            for b in BUILTIN_BACKENDS:
                try:
                    self._backend = globals()[b](self)
                    break
                except KeyError: pass
        
        elif not issubclass(backend, GpioInterface):
            raise RuntimeError('Invalid backend interface')
        else:
            self._backend = backend(self)
        
        if self._backend is None:
            raise RuntimeError('No builtin backends available: {}'.format(BUILTIN_BACKENDS))
    
    def setup(self, pin, mode):
        if mode not in self.MODES:
            raise TypeError("Invalid mode: {}".format(mode))
        if not isinstance(pin, list):
            pin = [pin]
        
        for p in pin:
            self._pins[p] = mode
            self._backend.setup(p, mode)
    
    def write(self, pin, state):
        if pin not in self._pins:
            raise IndexError("Pin not configured")
        
        if self._pins[pin] == modes.PWM:
            return Pwm(self._backend, pin)
        
        if mode != modes.OUT:
            raise TypeError("pin {} not configured for output".format(pin))
        
        self._backend.write(pin, state)
    
    def read(self, pin):
        if pin not in self._pins:
            raise IndexError("Pin not configured")
        if mode != modes.IN:
            raise TypeError("pin {} not configured for input".format(pin))
        
        return self._backend.read(pin)
    