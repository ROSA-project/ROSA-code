# postponed evaluation of annotations. With python 3.11, we won't need this
from __future__ import annotations
from shape import Shape
from position import Position
import intersection_instance as in_in

ObjectId = int  # type aliasing, since we might change ObjectId composition


class Object:
    def __init__(self, oid: ObjectId, shape: Shape, position: Position,
                 owner_object: Object):
        self.oid = oid
        self.shape = shape
        self.position = position
        self.__previous_position = position
        self.owner_object = owner_object
        self.dependent_objects: dict[ObjectId, Object] = {}
        self.__latest_intersections: list[in_in.IntersectionInstance] = []
        self._infinitesimal_intersection_occured: bool = False

    def add_dependent_object(self, obj: Object):
        self.dependent_objects[obj.oid] = obj
    
    def evolve(self, delta_t: float) -> dict[ObjectId, Object]:
        """Transitions the object and all its dependents to the next state.

        Args:
            delta_t: span of evolution in seconds

        Returns:
            A dictionary of all the new objects which are created by this object.
            These new objects will be added to the list of dependent objects.
        """

        # TODO: evolve should access to the list of intersections in this iteration.
        # TODO: evolve should actually change the state. We currently do not change
        # Position or Speed
        offspring_objects: dict[ObjectId, Object] = {}
        for oid in self.dependent_objects:
            offsprings = self.dependent_objects[oid].evolve(delta_t)
            offspring_objects.update(offsprings)

        return offspring_objects

    def set_intersections(self, intersections: list[in_in.IntersectionInstance]) -> None:
        """
        Registers this round's intersections
        if any infinitesimal intersection, calls handle_infinitesimal_intersection
        to decide on the consequences in the current evolution cycle
        note that the consequences on behavior of the robot will be handled in the 
        next evolution cycle
        """
        self.__latest_intersections = intersections.copy()
        self.__infinitesimal_intersection_occured = False
        for in_in in self.__latest_intersections:
            if in_in.is_infinitesimal():
                self.__infinitesimal_intersection_occured = True
                
        if self.__infinitesimal_intersection_occured:
            self.infinitesimal_intersection_immediate()
    
    def infinitesimal_intersection_immediate(self):
        """
        by default, we revert the position without reverting the rest of the state
        """
        self.revert_position()

    def update_position(self,new_position):
        self.__previous_position = self.position.copy()
        self.position = new_position.copy()

    def revert_position(self):
        self.position = self.__previous_position.copy()

    def visualize(self) -> list:
        """
        return the right position of object
        """
        position = [self.position.x, self.position.y ,self.position.phi]
        return position

    def dump_shape_info(self):
        return self.shape.dump_info()

    def bounding_box(self) -> Box:
        pass

    def get_required_delta_t(self) -> float:
        """returns the delta_t that this object requires to operate right.
           returns 0 if the objects declares no requirement.
        """
        return 0
        
    def time_to_die(self) -> bool:
        """Checks if object must cease to exist in the next iteration of the world.
        """
        return False

    def is_evolvable(self) -> bool:
        """Checks if object should be evolved directly by the world.
        """
        return not self.owner_object
