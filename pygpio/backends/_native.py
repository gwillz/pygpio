
import math, time, threading, select
from pygpio.interface import GpioInterface
from pygpio import modes

# pragma pylint: disable=protected-access

# TODO combine _addOutput, _addInput

def hertz_to_ms(freq, duty=0.50, multiplier=math.pow(10, 7)):
    space = int(1.0 / freq * multiplier)
    mark = int(space * duty)
    return mark, space

class NativeBackend(GpioInterface):
    PWM_PINS = {
        18: ('alt5', 0, 0),
        13: ('alt0', 0, 1),
        12: ('alt0', 1, 0),
        19: ('alt5', 1, 1)
    } #: pin -> func, chip, channel
    TICK = 0.1 #: time between export and gpio available (in seconds)
    POLL = 0.2 #: read timeout (in seconds)
    
    # chip-select, channel, property
    _PWM = '/sys/class/pwm/pwmchip{cs:d}/pwm{ch:d}/{prop}'
    _GPIO = '/sys/class/gpio/gpio{pin:d}/{prop}'
    _EXPORT = '/sys/class/gpio/{prop}'
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        self._last_error = None
        self._pwmfreq = wrapper.PWM_FREQ
        self._pwmduty = wrapper.PWM_DUTY
        
        self._out_pin = {}
        self._in_poll = select.poll()
        self._in_pin = {} #: pin -> mode, file, value
        self._in_file = {} #: fileno -> file, pin
        
        self._continue = True
        self._thread = threading.Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()
    
    def __del__(self):
        self._continue = False
        self._thread.join()
        
        for pin in self._in_pin:
            self._dropInput(pin, destroy=False)
        self._in_pin = {}
        
        # drop inputs before to avoid iterator errors
        for pin in self._wrapper._pins:
            self.clear(pin)
    
    def setup(self, pin, mode):
        if mode == modes.PWM:
            self._stopPwm(pin)
        else:
            m = 'in' if mode & modes._IN else 'out'
            
            self._write(self._EXPORT, pin, prop='export')
            time.sleep(self.TICK) # file ops are slow apparently
            self._write(self._GPIO, m, pin=pin, prop='direction')
            
            if pin in self._in_pin:
                self._dropInput(pin)
            
            if pin in self._out_pin:
                self._out_pin[pin].close()
                del self._out_pin[pin]
            
            if mode == modes.OUT:
                time.sleep(self.TICK)
                self._out_pin[pin] = open(self._GPIO.format(pin=pin, prop='value'), 'w')
            
            if mode & modes._IN:
                time.sleep(self.TICK)
                self._addInput(pin, mode)
            
        return True
    
    def clear(self, pin):
        mode = self._wrapper._pins[pin]
        
        if mode == modes.PWM:
            self._stopPwm(pin)
        else:
            self._dropInput(pin)
            
            if pin in self._out_pin:
                self._out_pin[pin].close()
            
            self._write(self._EXPORT, pin, prop='unexport')
    
    def write(self, pin, state):
        # self._write(self._GPIO, 1 if state else 0, pin=pin, prop='value')
        try:
            self._out_pin[pin].write('1' if state else '0')
            self._out_pin[pin].seek(0)
        except KeyError: pass # eh?
        
    def read(self, pin):
        return self._in_pin[pin][2]
        
    def writePwm(self, pin, state, freq=None, duty=None):
        if freq: self._pwmfreq = freq
        if duty: self._pwmduty = duty
        
        if state:
            self._startPwm(pin)
        else:
            self._stopPwm(pin)
    
    def _write(self, path, value, **props):
        try:
            with open(path.format(**props), 'w') as f:
                f.write(str(value))
        except IOError as e:
            self._last_error = e
    
    def _startPwm(self, pin):
        p = self.PWM_PINS[pin]
        mark, space = hertz_to_ms(self._pwmfreq, self._pwmduty)
        
        self._write(self._PWM, mark, cs=p[1], ch=p[2], prop='duty_cycle')
        self._write(self._PWM, space, cs=p[1], ch=p[2], prop='period')
        self._write(self._PWM, mark, cs=p[1], ch=p[2], prop='duty_cycle')
        self._write(self._PWM, 1, cs=p[1], ch=p[2], prop='enable')
    
    def _stopPwm(self, pin):
        p = self.PWM_PINS[pin]
        self._write(self._PWM, 0, cs=p[1], ch=p[2], prop='duty_cycle')
        self._write(self._PWM, 0, cs=p[1], ch=p[2], prop='enable')
    
    def _addInput(self, pin, mode):
        self._write(self._GPIO, modes._edge_name(mode), pin=pin, prop='edge')
        
        f = open(self._GPIO.format(pin=pin, prop='value'), 'rb+')
        v = self._readInput(f)
        
        self._in_pin[pin] = [mode, f, v]
        self._in_file[f.fileno()] = (f, pin)
        self._in_poll.register(f, select.POLLPRI | select.POLLERR)
        
    def _dropInput(self, pin, destroy=True):
        try:
            m, f, v = self._in_pin[pin] # pylint: disable=unused-variable
            self._in_poll.unregister(f)
            f.close()
            
            if destroy:
                del self._in_pin[pin]
        except KeyError: pass
    
    def _readInput(self, f):
        try:
            f.seek(0)
            return int(f.read()[0]) == 49 # '1' in ascii
        except (IOError, ValueError, IndexError) as e:
            self._last_error = e
    
    def _loop(self):
        timeout = int(self.POLL*1000)
        
        while self._continue:
             # this blocks
            for fd, ev in self._in_poll.poll(timeout): # pylint: disable=unused-variable
                f, pin = self._in_file[fd]
                mode, _, old_v = self._in_pin[pin]
                
                v = self._readInput(f)
                self._in_pin[pin][2] = v
                
                if v != old_v:
                    if v and mode & modes._RISING:
                        self._wrapper.onRising.fire(self._wrapper, pin)
                    elif not v and mode & modes._FALLING:
                        self._wrapper.onFalling.fire(self._wrapper, pin)
                
