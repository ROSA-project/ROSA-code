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

           Calculation the smallest bounding box,function moves
        the shape to the origin position,then rotates it with the
        corner points. After that,it calculates the dimensions of
        the box that is tangent to the farthest corners of the rotation.
        then returns the shape in last position, and bounding box have position
        Exactly the same position as shape.
        """
        # TODO: The following calculation is only for an upright cube
        r = self.radius
        h = self.height
        # Notice: Because the shape is symmetrical,
        # only the corner points of top disk are needed, then double the dimensions.
        points = [[r, 0, h / 2], [0, r, h / 2], [-r, 0, h / 2], [0, -r, h / 2]]
        new_x = list()
        new_y = list()
        new_z = list()
        for point in points:
            # Notice: At these angles, theta does not change the shape,
            # and because it is symmetrical, phi does not affect the shape.
            # then we replace them with 0.
            if position.theta % 180 == 0:
                new_point = Shape.rotation(point[0], point[1], point[2], 0, 0)
            else:
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

        return {"type": __class__.__name__, "dimension": [self.radius]}
