# pragma pylint: disable=bad-whitespace
HIGH     = True
LOW      = False
OUT      = 0
_IN      = 1
PWM      = 2
_RISING  = 4
_FALLING = 8
RISING   = _IN + _RISING
FALLING  = _IN + _FALLING
BOTH     = _IN + _RISING + _FALLING
IN       = BOTH

def _edge_name(mode):
    if mode == RISING:
        return 'rising'
    elif mode == FALLING:
        return 'falling'
    else:
        return 'both'
