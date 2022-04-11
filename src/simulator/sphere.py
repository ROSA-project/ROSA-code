from __future__ import annotations
from position import Position
from shape import Shape
from cube import Cube


class Sphere(Shape):
    def __init__(self, radius: float):
        Shape.__init__(self)
        self.radius = radius

    def dump_info(self) -> dict:
        """Returns the shape info required for visualization

        Returns:
            A dictionary with two keys: "type" is the shape's name, and "dimension" is a
            list of dimension numbers.
        """

        return {"type": __class__.__name__, "dimension": [self.radius]}



