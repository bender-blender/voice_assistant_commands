import time


class StopwatchProvider:

    start_time = None

    def start(self):
        self.start_time = time.time()

    def elapsed(self):
        if self.start_time is None:
            raise RuntimeError("Stopwatch has not been started.")
        return time.time() - self.start_time

    def reset(self):
        self.start_time = None
