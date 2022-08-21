import math

class CoordinateConversion():

    @staticmethod
    def cylindrical_to_cartesian_coordinate(r: float, theta: float, z: float) -> dict[str, float]:
        """
        Gets a point in the cylindrical coordinate system and converts it to cartesian coordinate system.
        Args:
            r: radial distance from the z-axis to the point,
            theta: the angle between the positive x-axis and the line segment from the origin to projection of the point
            in the xy-palne in degrees
            z: the usual z-coordinate
        """
        return {"x": r * math.cos(math.radians(theta)), "y": r * math.sin(math.radians(theta)), "z": z}

    @staticmethod
    def spherical_to_cartesian_coordinate(r: float, theta: float, phi: float):
        """
        Gets a point in the spherical coordinate system and converts it to cartesian coordinate system.
        Args:
            r: radial distance(distance to origin),
            theta: angle with respect to polar axis in degrees
            phi: azimuthal angle(angle of rotation from the initial meridian plane) in degrees
        """
        return {"x": r * math.cos((math.radians(phi))) * math.sin((math.radians(theta))),
                "y": r * math.sin((math.radians(phi))) * math.sin((math.radians(theta))),
                "z": r * math.cos((math.radians(theta)))}
