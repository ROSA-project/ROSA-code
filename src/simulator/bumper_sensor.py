from telnetlib import SE
from sensor import Sensor

class BumperSensor(Sensor):

    def sense(self) -> bool:
        if self._infinitesimal_intersection_occured:
            return True
        else:
            return False

