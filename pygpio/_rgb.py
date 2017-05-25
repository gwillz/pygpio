from pygpio._gpio import Gpio
from pygpio import modes, backends

# pragma pylint: disable=bad-whitespace

class _Color(object):
    def __init__(self, red, green, blue):
        self.red, self.green, self.blue = red, green, blue

class Rgb(object):
    black  = _Color(False, False, False)
    red    = _Color(True,  False, False)
    green  = _Color(False, True,  False)
    blue   = _Color(False, False, True)
    white  = _Color(True,  True,  True)
    yellow = _Color(True,  True,  False)
    aqua   = _Color(False, True,  True)
    purple = _Color(True,  False, True)
    colors = [black, red,    aqua,   green,
              white, purple, yellow, blue]
    
    BACKEND = backends.NativeBackend
    
    def __init__(self, red=12, green=19, blue=13, gpio=None):
        self._red = red
        self._green = green
        self._blue = blue
        
        self.gpio = gpio or Gpio(backend=self.BACKEND)
        self.gpio.setup([self._red, self._green, self._blue], modes.OUT)
    
    def set(self, color):
        self.gpio.write(self._red, color.red)
        self.gpio.write(self._green, color.green)
        self.gpio.write(self._blue, color.blue)
    
    def clear(self):
        self.set(self.black)
