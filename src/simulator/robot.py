from __future__ import annotations
from object import Object
from bumper_sensor import BumperSensor


class Robot(Object):
    def __init__(self, x: int, y: int, z: int, phi: int, theta: int):
        self.x = x
        self.y = y
        self.z = z
        self.phi = phi
        self.theta = theta
        #  super().__init__(oid, shape, position, owner_object)

    def evolve(self, bump: bool):
        """Transitions the object and all its dependents to the next state.

        Args:
            A Boolean bump signal

        Returns:
            The robot ID and its Position
        """
        if bump:
            print('bump')
            for i in range(5):
                self.phi += 10
        else:
            self.x += 1
            self.y += 1
        return [self.x, self.y, self.z, self.phi, self.theta]



