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

    def bounding_box(self) -> Box:
        """Returns smallest enclosing upright Box
        """

        # TODO: The following calculation is only for an upright cube
        # dimension calculations
        length = self.shape.length
        height = self.shape.height
        width = self.shape.width

        # position calculations
        x = self.position.x
        y = self.position.y
        z = self.position.z
        phi = self.position.phi
        theta = self.position.theta

        # assign return Arguments
        bb_cube = Cube(length, height, width)
        bb_position = Position(x, y, z, phi, theta)

        # return Box(1, bb_cube, bb_position)
        pass
