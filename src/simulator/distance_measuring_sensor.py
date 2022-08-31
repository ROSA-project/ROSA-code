import sensor
import object
import position
import cylinder
import object_registry
import beam
import copy
import numpy as np


class DistanceMeasuringSensor(sensor.Sensor):
    """
    it is a sensor that measures the distance of an object to where the sensor is located.
    """
    def __int__(self, oid: object.ObjectId, name: str, pos: position.Position,
                owner_object: object.Object, registry: object_registry.ObjectRegistry, parameter: float):
        self.position = pos
        new_position = copy.copy(self.position)
        new_position.x = 0.5 * parameter * np.cos(self.position.phi)
        new_position.y = 0.5 * parameter * np.sin(self.position.phi)
        new_position.theta = 90

        self.beam_object = beam.Beam(registry.get_next_available_id(), name, cylinder.Cylinder(0, parameter),
                                     new_position, owner_object, registry)

    def sense(self) -> float:
        """
        it measures the distance between the robot and any object.
        if it isn't in the range, it returns an unreasonable number.
        """
        for in_in in self.beam_object._latest_intersections:
            if in_in.does_intersect():
                delta_x = in_in.get_intersection_point()[0][0] - self.position.x
                delta_y = in_in.get_intersection_point()[0][1] - self.position.y
                distance = np.sqrt(delta_x**2 + delta_y**2)
                return distance
            else:
                return -1
