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

        Calculate the smallest bounding box. The function
        moves the shape to the coordinate origin,calculates
        the corner points of its dimensions and rotates it.
        The box is surrounded by the farthest rotated points.
        Then it returns the shape in the last position. The bounding box
        has the exact same position as the shape.
        """
        l = self.length
        w = self.width
        h = self.height
        # Because the cube has symmetry, we only need the top side points of the disk.
        # We calculate the distance of the farthest points and then get the dimensions
        # of the bounding box. Note, since we used the top points, because of symmetry,
        # we double the dimensions of the bounding box so that the box surrounds the bottom
        # points of the disk.
        points = [[l / 2, w / 2, h / 2], [-l / 2, w / 2, h / 2],
                  [l / 2, -w / 2, h / 2], [-l / 2, -w / 2, h / 2]]
        new_x = list()
        new_y = list()
        new_z = list()
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
