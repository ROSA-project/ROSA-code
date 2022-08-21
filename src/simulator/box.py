from __future__ import annotations
import position
import object as obj
import object_registry
import shape
import cube


class Box(obj.Object):
    def __init__(self, oid: obj.ObjectId, name: str, cube: cube.Cube, position: position.Position,
                 owner_object: obj.Object, registry: object_registry.ObjectRegistry):
        # if not isinstance(cube, cube.Cube):
        #     raise ValueError("A Box object must have Cube shape")

        obj.Object.__init__(self, oid, name, cube, position, owner_object, registry)
