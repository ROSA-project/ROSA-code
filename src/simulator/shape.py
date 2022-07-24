from __future__ import annotations
from position import Position
from numpy import cos, sin, deg2rad, dot


class Shape:
    def __init__(self):
        pass

    def bounding_box(self, position: Position):
        """Returns Box as an Object
        """
        pass

    def dump_info(self):
        pass

    def rotation(x: float, y: float, z: float, phi: float, theta: float) -> list[float]:
        """rotate the point by angles
        Args:
            x,y,z : coordinate of point in Cartesian
            phi : angle of rotation about z-axes respectively
            theta : angle of rotation about y-axes respectively
        Return:
            list of new coordinate point after rotation
        """
        cos_theta = cos(deg2rad(theta))
        cos_phi = cos(deg2rad(phi))
        sin_theta = sin(deg2rad(theta))
        sin_phi = sin(deg2rad(phi))
        old_point = [x, y, z]
        rotation_theta = [[cos_theta, 0, sin_theta],
                          [0, 1, 0],
                          [-sin_theta, 0, cos_theta]]
        rotation_phi = [[cos_phi, -sin_phi, 0],
                        [sin_phi, cos_phi, 0],
                        [0, 0, 1]]
        new_point = dot(rotation_phi, dot(rotation_theta, old_point))
        return new_point
