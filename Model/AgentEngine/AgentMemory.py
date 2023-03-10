from collections import OrderedDict
import time

class AgentMemoryTimedDict:
    def __init__(self, expiry_time):
        self.expiry_time = expiry_time
        self.data = OrderedDict()

    def get(self, key):
        self.cleanup()
        if key in self.data:
            return self.data[key]

    def set(self, key, value, timestamp):
        self.cleanup()
        self.data[key] = (value, timestamp)

    def contains(self, key):
        self.cleanup()
        return key in self.data

    def get_n_most_recent(self, n):
        self.cleanup()
        return [(key, value[0], value[1]) for key, value in list(self.data.items())[-n:]]

    def cleanup(self):
        
        current_time = time.time()
        expired_keys = []
        for key, value in self.data.items():
            if current_time - value[1] >= self.expiry_time:
                expired_keys.append(key)
        for key in expired_keys:
            del self.data[key]