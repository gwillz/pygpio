from abc import ABCMeta, abstractmethod

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
    def read(self, pin):
        pass
    
    @abstractmethod
    def writePwm(self, pin, state, freq=None):
        pass
