
from gpio.backends._native import NativeBackend
try:
    from gpio.backends._rpi import RpiBackend
except ImportError: pass
try:
    from gpio.backends._wiring_soft import WiringBackend
    from gpio.backends._wiring_hard import WiringHardBackend
except ImportError: pass
