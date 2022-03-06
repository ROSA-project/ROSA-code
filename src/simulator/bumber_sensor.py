from __future__ import annotations
from sensor import Sensor


class BumperSensor(Sensor):
    """In version 0: senses a hit after a random amount of time (e.g., of 10 iteration)

    Args:
        No Arguments included!

    Returns:
        Return a boolean value as a hit: Trigger.

    Note: In the next version we should consider the Intersection Instance
    from the world as a trigger input.
    """

    def __init__(self, oid: ObjectId, shape: Shape, position: Position, owner_object: Object):
        super().__init__(oid, shape, position, owner_object)

    dummy_counter = 0  # A counter for sensing a random hit

    def sense(self) -> bool:

        BumperSensor.dummy_counter += 1

        if BumperSensor.dummy_counter == 10:
            BumperSensor.dummy_counter = 0
            return True
        else:
            return False
