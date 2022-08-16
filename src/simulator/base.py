import object
from position import Position
from shape import Shape
import object_registry
from robot import Robot
import numpy as np

RadioID = str  # type aliasing, since we might change RadioID composition


class Base(object.Object):
    """
    Object for keeping the robot and moving between it, etc.
    The robot receives information from this object, such as distance.
    """
    def __init__(self, oid: object.ObjectId, name: str, shape: Shape, position: Position,
                 owner_object: object.Object, registry: object_registry.ObjectRegistry,
                 rid: RadioID, standard_deviation: float):
        super().__init__(oid, name, shape, position, owner_object, registry)
        self.radio_id = rid
        self.standard_deviation = standard_deviation

    def get_distance(self, robot: Robot) -> float:
        delta_x = self.position.x - robot.position.x
        delta_y = self.position.y - robot.position.y
        delta_z = self.position.z - robot.position.z
        true_distance = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
        distance = true_distance + np.random.normal(loc=0, scale=self.standard_deviation)
        return distance

    def evolve(self, delta_t: float):
        pass
