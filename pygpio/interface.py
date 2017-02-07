from abc import ABCMeta, abstractmethod

class GpioInterface(object, metaclass=ABCMeta):
    def __init__(self, wrapper):
        self._wrapper = wrapper
    
    def _eventCallback(self, pin):
        self._wrapper.onEvent.fire(self._wrapper, pin)
    
    @abstractmethod
    def setup(self, pin, mode):
        pass
    
    @abstractmethod
    def clear(self, pin):
        pass
    
    @abstractmethod
    def write(self, pin, state):
        pass
    
    @abstractmethod
    def read(self, pin):
        pass
    
    @abstractmethod
    def writePwm(self, pin, state, freq=None, duty=None):
        pass
