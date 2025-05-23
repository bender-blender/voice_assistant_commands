import time
from stark import Response

class Stopwatch:
    
    start_time = None

    def start(self):
        self.start_time = time.time()

    def elapsed(self):
        return time.time() - self.start_time