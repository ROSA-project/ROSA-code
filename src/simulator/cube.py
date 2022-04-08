from __future__ import annotations
from shape import Shape
from position import Position
# from box import Box
import box


class Cube(Shape):
    def __init__(self, length: float, height: float, width: float):
        self.length = length
        self.height = height
        self.width = width

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

    def dump_info(self) -> dict:
        """Returns the shape info required for visualization

        Returns:
            A dictionary with two keys: "type" is the shape's name, and "dimension" is a
            list of dimension numbers.
        """
        return {"type": __class__.__name__, "dimension": [self.length, self.height]}
