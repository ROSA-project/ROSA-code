from object import Object, ObjectId
from shape import Shape
from position import Position
from sensor import Sensor


class BumperSensor(Sensor):
    """In version 0: senses a hit after a random amount of time

    Args:
        reader: Read the input boolean
        action: Sense a trigger in input and do an action
        #TODO you can define any action as a method!

    Returns:
        Return a boolean value as a hit: Trigger.

    Note: In the next version we should consider the Intersection Instance
    from the world as a trigger input.
    """
    def __init__(self, reader, action, oid: ObjectId, shape: Shape, position: Position, owner_object: Object):
        super().__init__(oid, shape, position, owner_object)
        self.reader = reader
        self.action = action
        self.last_value = reader()  # initialise value

    def sense(self) -> bool:
        new_value = self.reader()
        if new_value and not self.last_value:
            self.action()
        self.last_value = new_value
        return self.last_value



