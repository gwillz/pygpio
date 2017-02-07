
from pygpio.backends._native import NativeBackend
try:
    from pygpio.backends._rpi import RpiBackend
except ImportError: pass
try:
    from pygpio.backends._wiring_soft import WiringBackend
    from pygpio.backends._wiring_hard import WiringHardBackend
except ImportError: pass
