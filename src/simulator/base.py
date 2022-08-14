from object import Object, ObjectId
from position import Position
from shape import Shape
from object_registry import ObjectRegistry
from robot import Robot
import numpy as np

RadioID = str  # type aliasing, since we might change RadioID composition


class Base(Object):
    def __init__(self, oid: ObjectId, name: str, shape: Shape, position: Position,
                 owner_object: Object, registry: ObjectRegistry, rid: RadioID, error: int):
        super().__init__(oid, name, shape, position, owner_object, registry)
        self.radio_id = rid
        self.error = error

    def get_distance(self, robot: Robot) -> float:
        delta_x = self.position.x - robot.position.x
        delta_y = self.position.y - robot.position.y
        delta_z = self.position.z - robot.position.z
        true_distance = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
        distance = true_distance + np.random.normal(loc=0, scale=self.error)
        return distance

    def evolve(self):
        pass
