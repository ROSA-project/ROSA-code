# postponed evaluation of annotations. With python 3.11, we won't need this
from __future__ import annotations
from shape import Shape
from position import Position
import intersection_instance as in_in
import copy
import logger

ObjectId = int  # type aliasing, since we might change ObjectId composition


class Object:
    def __init__(self, oid: ObjectId, name: string, shape: Shape, position: Position,
                 owner_object: Object):
        self.oid = oid
        self.name = name
        self.shape = shape
        # TODO we should do this deepcopy for all? a nicer way?
        self.position = position
        self.__previous_position = position
        self.owner_object = owner_object
        self.dependent_objects: dict[ObjectId, Object] = {}
        self._latest_intersections: list[in_in.IntersectionInstance] = []
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
        self._latest_intersections = copy.copy(intersections)
        self._infinitesimal_intersection_occured = False
        for in_in in self._latest_intersections:
            if in_in.does_intersect() and in_in.is_infinitesimal():
                self._infinitesimal_intersection_occured = True
                
        if self._infinitesimal_intersection_occured:
            self.infinitesimal_intersection_immediate()
    
    def infinitesimal_intersection_immediate(self):
        """
        by default, we revert the position without reverting the rest of the state
        """
        logger.Logger.add_line("infinitestimal intersection detected, reverting position (default Object behavior)")
        self.revert_position()

    def update_position(self,new_position):
        """
        all changes to the position must go through this function
        This is to ensure we keep the state. 
        # TODO how to enforce this?
        """
        self.__previous_position = copy.copy(self.position)
        self.position = copy.copy(new_position)

    def revert_position(self):
        # TODO leaves the position and previous position the same.
        # better to somehow invalidate previous position? (same should happen in
        # constructor where these two are again the same)
        self.position = copy.copy(self.__previous_position)

    def visualize(self) -> list:
        """
        return the right position of object
        """
        position = [self.position.x, self.position.y ,self.position.phi]
        return position

    def dump_shape_info(self):
        if self.shape is None:
            return None
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
