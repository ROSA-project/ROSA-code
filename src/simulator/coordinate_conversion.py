import math


class CoordinateConversion():
    @classmethod
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
