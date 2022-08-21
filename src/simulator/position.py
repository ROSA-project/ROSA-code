from __future__ import annotations
import numpy as np
import math
from coordinate_conversion import CoordinateConversion
from pyquaternion import Quaternion
from numpy import linalg as LA


class Position:
    def __init__(self, x: int, y: int, z: int, phi: int, theta: int):
        self.x = x
        self.y = y
        self.z = z
        self.phi = phi
        self.theta = theta


    def calculate_orientation_quaternion(self, height: float) -> Quaternion:
        """
        Returns the Orientation Quaternion
        """
        # TODO: sync this with the saeed's idea of each shape having an Axis Unit Vector
        cartesian_coordinate_of_orientation = CoordinateConversion.spherical_to_cartesian_coordinate(height / 2,
                                                                                                     self.theta,
                                                                                                     self.phi)
        orientation_vector = [cartesian_coordinate_of_orientation["x"], cartesian_coordinate_of_orientation["y"],
                              cartesian_coordinate_of_orientation["z"]]
        cartesian_coordinate_of_default_orientation = CoordinateConversion.spherical_to_cartesian_coordinate(height / 2,
                                                                                                             0, 0)
        default_orientation_vector = [cartesian_coordinate_of_default_orientation["x"],
                                      cartesian_coordinate_of_orientation["y"],
                                      cartesian_coordinate_of_default_orientation["z"]]
        if math.isclose(np.dot(default_orientation_vector, orientation_vector), LA.norm(default_orientation_vector) * LA.norm(orientation_vector)):
            quaternion = Quaternion(axis= default_orientation_vector, degrees=0)
            return quaternion.normalised
        elif math.isclose(np.dot(default_orientation_vector, orientation_vector), -1*LA.norm(default_orientation_vector) * LA.norm(orientation_vector)):
            quaternion = Quaternion(axis= default_orientation_vector, degrees=180)
            return quaternion.normalised
        else:
            cross_product = np.cross(default_orientation_vector, orientation_vector)
            norm = LA.norm(cross_product)
            axis = [cross_product[0] / norm, cross_product[1] / norm, cross_product[2] / norm]
            angle_of_rotation = math.degrees(math.atan(norm / (np.dot(default_orientation_vector, orientation_vector))))

            return Quaternion(axis=axis, degrees=angle_of_rotation).normalised

