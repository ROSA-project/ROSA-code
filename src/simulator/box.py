from __future__ import annotations
from position import Position
from object import Object, ObjectId
import shape
import cube


class Box(Object):
    def __init__(self, oid: ObjectId, cube: cube.Cube, position: Position,
                 owner_object: Object):
        # if not isinstance(cube, cube.Cube):
        #     raise ValueError("A Box object must have Cube shape")

        Object.__init__(self, oid, cube, position, owner_object)
