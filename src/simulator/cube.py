from __future__ import annotations
from shape import Shape
from position import Position
from box import Box


class Cube(Shape):
    def __init__(self, length: float, height: float, width: float):
        self.length = length
        self.height = height
        self.width = width

    def bounding_box(self, position: Position) -> Box:
        """Returns smallest enclosing upright Box
        """
        l = self.length
        w = self.width
        h = self.height
        points = [[l / 2, w / 2, h / 2], [-l / 2, w / 2, h / 2],
                  [l / 2, -w / 2, h / 2], [-l / 2, -w / 2, h / 2],
                  [l / 2, w / 2, -h / 2], [-l / 2, w / 2, -h / 2],
                  [l / 2, -w / 2, -h / 2], [-l / 2, -w / 2, -h / 2]]
        new_x, new_y, new_z = [], [], []
        for point in points:
            new_point = Shape.rotation(point[0], point[1], point[2], position.phi, position.theta)
            new_x.append(new_point[0])
            new_y.append(new_point[1])
            new_z.append(new_point[2])
        length = 2 * max([abs(x) for x in new_x])
        width = 2 * max([abs(y) for y in new_y])
        height = 2 * max([abs(z) for z in new_z])
        bounding_box = Box(oid=None, name=None, cube=Cube(length=length, width=width, height=height),
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
        return {"type": __class__.__name__, "dimension": [self.length, self.width]}
