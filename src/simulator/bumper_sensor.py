from telnetlib import SE
from sensor import Sensor

class BumperSensor(Sensor):
    elapsed_time = 0
    def sense(self,delta_t) -> bool:
        # a dummy implementation for v0

        self.elapsed_time += delta_t
        if self.elapsed_time >= 3: #in seconds
            self.elapsed_time = 0
            return True
        else:
            return False

