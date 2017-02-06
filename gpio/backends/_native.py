"""
# download/compile/install librpip

cp distro/arch/pwm-init.service /etc/systemd/system
sudo systemctl daemon-reload`
sudo systemctl enable pwm-init
sudo su -c 'echo dtoverlay=pwm,pin=18,func=2 > /boot/config.txt'
sudo reboot
"""

# TODO read(pin)
# TODO events callbacks

import math, time
from gpio.interface import GpioInterface
from gpio import modes

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
    } # pin, func, chip, channel
    TICK = 0.1
    
    # chip-select, channel, property
    _PWM = '/sys/class/pwm/pwmchip{cs:d}/pwm{ch:d}/{prop}'
    _GPIO = '/sys/class/gpio/gpio{pin:d}/{prop}'
    _EXPORT = '/sys/class/gpio/{prop}'
    
    def __init__(self, wrapper):
        GpioInterface.__init__(self, wrapper)
        self._last_error = None
        self._pwmfreq = wrapper.PWM_FREQ
        self._pwmduty = wrapper.PWM_DUTY
    
    def setup(self, pin, mode):
        if mode == modes.PWM:
            self._stopPwm(pin)
        else:
            m = "out" if mode == modes.OUT else "in"
            self._write(self._EXPORT, pin, prop='export')
            time.sleep(self.TICK) # file ops are slow apparently
            self._write(self._GPIO, m, pin=pin, prop='direction')
            
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
        # return None
        raise NotImplementedError("TODO read(pin)")
    
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
    
