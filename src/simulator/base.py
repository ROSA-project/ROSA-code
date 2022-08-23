import object
import position
import shape
import object_registry
import numpy as np


class Base(object.Object):
    """
    A physical station, primarily in charge of communicating with robots
    and facilitating their navigation by transmitting their (estimated) distances with the base.
    """

    def __init__(self, oid: object.ObjectId, name: str, shape: shape.Shape, position: position.Position,
                 owner_object: object.Object, registry: object_registry.ObjectRegistry,
                 standard_deviation: float, time_using: float):
        super().__init__(oid, name, shape, position, owner_object, registry)
        self.standard_deviation = standard_deviation
        self.__timer = 0
        self.__time_using = time_using

    def get_distance(self, position: position.Position) -> float:
        """
        It calculates and returns the distance between itself and the robot with some error.
        """
        # TODO: Temporarily, this method takes a position. It should change later.

        if self.can_get:
            delta_x = self.position.x - position.x
            delta_y = self.position.y - position.y
            delta_z = self.position.z - position.z
            true_distance = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
            distance = true_distance + np.random.normal(loc=0, scale=self.standard_deviation)
            self.__timer = 0
            return distance

    def can_get(self) -> bool:
        """
        To allow the request
        """
        # TODO: This number is temporary, until we decide on it
        step_round = 3
        if np.round(abs(self.__timer - self.__time_using), step_round) == 0:
            return True

        return False

    def evolve(self, delta_t: float) -> dict[object.ObjectId, object.Object]:
        """
        Just like in the object class, only time is added to the timer
        """
        self.__timer += delta_t
        return object.Object.evolve(self, delta_t)