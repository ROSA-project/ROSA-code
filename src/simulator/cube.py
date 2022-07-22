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
        pass

    def dump_info(self) -> dict:
        """Returns the shape info required for visualization

        Returns:
            A dictionary with two keys: "type" is the shape's name, and "dimension" is a
            list of dimension numbers.
        """
        return {"type": __class__.__name__, "dimension": [self.length, self.width]}
