import object
from position import Position
from shape import Shape
import object_registry
from robot import Robot
import numpy as np

RadioID = object.ObjectId


class Base(object.Object):
    """
    A physical station, primarily in charge of communicating with robots
    and facilitating their navigation by transmitting their (estimated) distances with the base.
    """

    def __init__(self, oid: object.ObjectId, name: str, shape: Shape, position: Position,
                 owner_object: object.Object, registry: object_registry.ObjectRegistry,
                 rid: RadioID, standard_deviation: float):
        super().__init__(oid, name, shape, position, owner_object, registry)
        self.radio_id = rid
        self.standard_deviation = standard_deviation
        self.__timer = 0

    def get_distance(self, position: Position):
        """
        It calculates and returns the distance between itself and the robot with some error.
        """
        if self.__timer % 0.05 == 0:
            delta_x = self.position.x - position.x
            delta_y = self.position.y - position.y
            delta_z = self.position.z - position.z
            true_distance = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
            distance = true_distance + np.random.normal(loc=0, scale=self.standard_deviation)
            return distance
        else:
            return None

    def evolve(self, delta_t: float) -> dict[object.ObjectId, object.Object]:
        """
        Just like in the object class, only time is added to the timer
        """
        self.__timer += delta_t
        offspring_objects: dict[object.ObjectId, object.Object] = {}
        for oid in self.dependent_objects:
            offsprings = self.dependent_objects[oid].evolve(delta_t)
            offspring_objects.update(offsprings)

        return offspring_objects
