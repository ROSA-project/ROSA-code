from __future__ import annotations
from object import Object


class Sensor(Object):
    # def sense(self, intersections: list[IntersectionInstance]) -> bool #for the next version
    def __init__(self, oid: ObjectId, shape: Shape, position: Position, owner_object: Object):
        super().__init__(oid, shape, position, owner_object)

    def sense(self):
        pass  # this method is going to be overridden in the children classes of BumperSensor
