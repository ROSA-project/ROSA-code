from __future__ import annotations
from position import Position
from shape import Shape
from box import Box
from cube import Cube


class Cylinder(Shape):
    def __init__(self, radius: float, height: float):
        Shape.__init__(self)
        self.radius = radius
        self.height = height

    def bounding_box(self, position: Position) -> Box:
        """Returns smallest enclosing upright Box
        """

        # TODO: The following calculation is only for an upright cube
        # dimension calculations
        r = self.radius
        h = self.height
        points = [[r, 0, h / 2], [0, r, h / 2], [-r, 0, h / 2], [0, -r, h / 2]]
        new_x, new_y, new_z = [], [], []
        for point in points:
            if position.theta in [0,180,-180]:
                new_point = Shape.rotation(point[0], point[1], point[2], 0, 0)
            else:
                new_point = Shape.rotation(point[0], point[1], point[2], position.phi, position.theta)
            new_x.append(new_point[0])
            new_y.append(new_point[1])
            new_z.append(new_point[2])
        length = 2 * max([abs(x) for x in new_x])
        width = 2 * max([abs(y) for y in new_y])
        height = 2 * max([abs(z) for z in new_z])
        bounding_box = Box(oid=None,name=None,cube=Cube(length= length,width= width,height= height),
                           position=Position(position.x, position.y, position.z, 0, 0),
                           owner_object=None,
                           registry=None)
        return bounding_box

    def dump_info(self) -> dict:
        """Returns the shape info required for visualization

        Returns:
            A dictionary with two keys: "type" is the shape's name, and "dimension" is a
            list of dimension numbers.
        """

        return {"type": __class__.__name__, "dimension": [self.radius]}
