from telnetlib import SE
from sensor import Sensor


class BumperSensor(Sensor):
    elapsed_time_sec: int = 0

    def sense(self, delta_t) -> bool:
        # a dummy implementation for v0

        self.elapsed_time_sec += delta_t
        if self.elapsed_time_sec >= 3:
            self.elapsed_time_sec = 0
            return True
        else:
            return False

