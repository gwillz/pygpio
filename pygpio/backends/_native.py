
# TODO read(pin)
# TODO events callbacks

import math, time, threading
from avent import wait_for
from pygpio.interface import GpioInterface
from pygpio import modes

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
    } #: pin: func, chip, channel
    TICK = 1.0/50
    
    # chip-select, channel, property
    _PWM = '/sys/class/pwm/pwmchip{cs:d}/pwm{ch:d}/{prop}'
    _GPIO = '/sys/class/gpio/gpio{pin:d}/{prop}'
    _EXPORT = '/sys/class/gpio/{prop}'
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        self._last_error = None
        self._pwmfreq = wrapper.PWM_FREQ
        self._pwmduty = wrapper.PWM_DUTY
        
        self._inputs = {} #: pin: mode, file, bounce
        self._continue = True
        self._thread = threading.Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()
    
    def __del__(self):
        self._continue = False
        wait_for(self._thread.is_alive, state=False)
        for pin in self._inputs:
            self._inputs[pin][1].close()
    
    def setup(self, pin, mode):
        if mode == modes.PWM:
            self._stopPwm(pin)
        else:
            m = 'in' if mode & modes.IN else 'out'
            
            self._write(self._EXPORT, pin, prop='export')
            time.sleep(self.TICK*5) # file ops are slow apparently
            self._write(self._GPIO, m, pin=pin, prop='direction')
            
            if mode & modes._EVENT:
                if mode == modes.RISING: edge = 'rising'
                elif mode == modes.FALLING: edge = 'falling'
                else:
                    edge = 'both'
                    mode = modes.BOTH
                
                time.sleep(self.TICK*5)
                self._write(self._GPIO, edge, pin=pin, prop='edge')
                
                if pin in self._inputs:
                    self._inputs[pin][1].close()
                    del self._inputs[pin]
                
                f = open(self._GPIO.format(pin=pin, prop='value'), 'r')
                self._inputs[pin] = [mode, f, False]
            
            elif pin in self._inputs:
                self._inputs[pin][1].close()
                del self._inputs[pin]
            
        return True
    
    def clear(self, pin):
        mode = self._wrapper._pins[pin]
        if mode == modes.PWM:
            self._stopPwm(pin)
        else:
            self._write(self._EXPORT, pin, prop='unexport')
    
    def write(self, pin, state):
        self._write(self._GPIO, 1 if state else 0, pin=pin, prop='value')
        
    def read(self, pin):
        mode = self._wrapper._pins[pin]
        
        if mode & modes._EVENT:
            return self._inputs[pin][2] > 0
        else:
            with open(self._GPIO.format(pin=pin, prop='value'), 'r') as f:
                return f.read()[0] == '1'
        
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
        
        # time.sleep(self.TICK)
    
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
    
    def _loop(self):
        while self._continue:
            for pin in self._inputs:
                mode, f, bounce = self._inputs[pin]
                
                try:
                    f.seek(0)
                    v = f.read()[0]
                except IOError as e:
                    self._last_error = e
                    continue
                
                if v == '1' and bounce == 0:
                    self._inputs[pin][2] = self._wrapper.IN_BOUNCE
                    
                    if mode & modes._RISING:
                        self._wrapper.onRising.fire(self, pin)
                    elif mode & modes._FALLING:
                        self._wrapper.onFalling.fire(self, pin)
                
                elif v == '1' and bounce > 0:
                    self._inputs[pin][2] -= self.TICK
                else:
                    self._inputs[pin][2] = 0
                
                time.sleep(self.TICK)
