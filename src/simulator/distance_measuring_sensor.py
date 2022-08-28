import sensor
import object
import position
import cylinder
import object_registry
import beam


class DistanceMeasuringSensor(sensor.Sensor):
    def __int__(self, oid: object.ObjectId, name: str, pos: position.Position,
                owner_object: object.Object, registry: object_registry.ObjectRegistry, parameter: float):
        self.beam_object = beam.Beam(registry.get_next_available_id(), name, cylinder.Cylinder(0, parameter),
                                     pos, owner_object, registry)

    def sense(self):
        for in_in in self.beam_object._latest_intersections:
            if in_in.does_intersect() and in_in.is_infinitesimal():
                return self.beam_object.shape.height

