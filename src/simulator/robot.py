from __future__ import annotations
from object import Object
from position import Position
from object import ObjectId
from shape import Shape


class Robot(Object):
    def __init__(self, oid: ObjectId, shape: Shape, position: Position, owner_object: Object):
        super().__init__(oid, shape, position, owner_object)

    def evolve(self):
        pass  # this method is going to be overridden in the children classes of VacuumCleaner

