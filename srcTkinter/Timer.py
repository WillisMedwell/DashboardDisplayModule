import time

class TimeUnit():
    _time = None
    def __init__(self, time):
        self._time = time
    
    def s(self):
        return self._time

    def ms(self):
        return self._time*1e+3

    def ns(self):
        return self._time*1e+9


class Timer():
    _start = None
    _last_lap = None
    _sleep_duration = None
    def __init__(self):
        self._start = time.perf_counter()

    def reset(self):
        self._last_lap = self.get_elapsed().s()
        self._start = time.perf_counter()
        self._sleep_duration = None
    
    def get_elapsed(self):
        if self._sleep_duration == None:
            return TimeUnit(time.perf_counter() - self._start)
        else:
            return TimeUnit(time.perf_counter() - self._start + self._sleep_duration)

    def get_last_lap(self):
        return TimeUnit(self._last_lap)

    def sleep(self, duration):
        if duration > 0:
            self._sleep_duration = duration
            time.sleep(self._sleep_duration)

