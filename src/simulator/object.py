# postponed evaluation of annotations. With python 3.11, we won't need this
from __future__ import annotations
from shape import Shape
from position import Position
from intersection_instance import IntersectionInstance

ObjectId = int  # type aliasing, since we might change ObjectId composition


class Object:
    def __init__(self, oid: ObjectId, shape: Shape, position: Position, owner_object: Object):
        self.oid = oid
        self.shape = shape
        self.position = position
        self.owner_object = owner_object
        self.dependent_objects: dict[ObjectId, Object] = {}

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

        # add the new offsprings to the list of dependents
        self.dependent_objects.update(offspring_objects)
        return offspring_objects

    def set_intersections(self, intersections: list[IntersectionInstance]) -> None:
        """Registers this round's intersections to be later used by evolve().
        """
        # TODO: should it be simply stored in a member variable?
        pass
    
    def visualize(self):
        # TODO: define return type
        pass
    
    def bounding_box(self):
        # TODO: define return type
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
