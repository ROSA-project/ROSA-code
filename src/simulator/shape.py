from __future__ import annotations
from position import Position
from numpy import cos, sin, deg2rad


class Shape:
    def __init__(self):
        pass

    def bounding_box(self, position: Position):
        """Returns Box as an Object
        """
        pass

    def dump_info(self):
        pass

    def rotation(x: float, y: float, z: float, phi: float, theta: float):
        cos_theta = cos(deg2rad(theta))
        cos_phi = cos(deg2rad(phi))
        sin_theta = sin(deg2rad(theta))
        sin_phi = sin(deg2rad(phi))
        new_x = round(x * cos_phi*cos_theta - y * sin_phi + z * sin_theta * cos_phi, 3)
        new_y = round(x * sin_phi*cos_theta + y * cos_phi + z * sin_phi * sin_theta, 3)
        new_z = round(-x * sin_theta + z * cos_theta, 3)
        return [new_x, new_y, new_z]
