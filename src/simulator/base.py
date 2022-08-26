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

    def __init__(self, oid: object.ObjectId, name: str, shp: shape.Shape, pos: position.Position,
                 owner_object: object.Object, registry: object_registry.ObjectRegistry,
                 standard_deviation: float, no_response_gap: float):
        super().__init__(oid, name, shp, pos, owner_object, registry)
        self.standard_deviation = standard_deviation
        self.__timer: float = 0
        self.__no_response_gap = no_response_gap

    def get_distance(self, pos: position.Position) -> float:
        """
        It calculates and returns the distance between itself and the robot with some error.
        In the current way, true distance is the distance between anchor points of the objects
        base and robot, i.e. probably their center points. This means that the true distance doesn't
        consider the dimensions of the objects
        """
        # TODO: Temporarily, this method takes the position as argument, meaning that the robot
        #       has access to its position, which is absurd. This has to be handled later.

        if self.can_get():
            delta_x = self.position.x - pos.x
            delta_y = self.position.y - pos.y
            delta_z = self.position.z - pos.z
            true_distance = np.sqrt(delta_x ** 2 + delta_y ** 2 + delta_z ** 2)
            # TODO: error model and distribution can later become a parameter too.
            distance = true_distance + np.random.normal(loc=0, scale=self.standard_deviation)
            self.__timer = 0
            return distance
        else:
            return -1

    def can_get(self) -> bool:
        """
        to keep track of the no response gap between consecutive get_distance requested.
        note that if multiple robots use one base, the timer is not kept per robot.
        we could add this later
        """
        if self.__timer >= self.__no_response_gap:
            return True
        else:
            return False

    def evolve(self, delta_t: float) -> dict[object.ObjectId, object.Object]:
        """
        Just like in the object class, only time is added to the timer
        """
        self.__timer += delta_t
        return object.Object.evolve(self, delta_t)
