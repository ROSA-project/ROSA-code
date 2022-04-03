from __future__ import annotations
from cube import Cube
from position import Position
from object import Object, ObjectId
from shape import Shape


class Box(Object):
    def __init__(self, oid: ObjectId, shape: Shape, position: Position,
                 owner_object: Object):
        
        Object.__init__(self, oid, shape, position, owner_object)
        
        if not isinstance(self.shape, Cube):
            raise Exception("A Box object must have Cube shape")
