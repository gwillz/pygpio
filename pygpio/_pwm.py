import time, sys

class Pwm(object):
    def __init__(self, backend, pin):
        self._pin = pin
        self._backend = backend
    
    def start(self, freq):
        self._backend.writePwm(self._pin, True, freq)
    
    def stop(self):
        self._backend.writePwm(self._pin, False)
    
    def setFrequency(self, freq):
        self._backend.writePwm(self._pin, None, freq)
    
    def playScore(self, score):
        for i in score[1:]:
            if not i:
                time.sleep(score[0] + score[0]/2)
                continue
            
            self.start(i)
            time.sleep(score[0])
            self.stop()
            time.sleep(score[0]/2)



if sys.version_info.major > 2 and sys.version_info.minor >= 4:
    import asyncio
    
    @asyncio.coroutine
    def playAsync(self, score):
        for i in score[1:]:
            if not i:
                yield from asyncio.sleep(score[0] + score[0]/2)
                continue
    
            self.start(i)
            yield from asyncio.sleep(score[0])
            self.stop()
            yield from asyncio.sleep(score[0]/2)
    
    Pwm.playAsync = playAsync
