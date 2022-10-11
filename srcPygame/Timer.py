import time

class TimeUnit():
    def __init__(self, time):
        self._time = time
    
    def s(self):
        return self._time

    def ms(self):
        return self._time*1e+3

    def ns(self):
        return self._time*1e+9


class Timer():
    def __init__(self):
        self._start = time.perf_counter()
        self._last_lap = time.perf_counter()

    def Reset(self):
        self._last_lap = self.GetElapsed().s()
        self._start = time.perf_counter()
    
    def GetElapsed(self):
        return TimeUnit(time.perf_counter() - self._start)

    def GetLastLap(self):
        return TimeUnit(self._last_lap)

    def Sleep(self, duration):
        if duration > 0:
            time.sleep(duration)

