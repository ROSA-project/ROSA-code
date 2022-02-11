import time

from intersection_instance import IntersectionInstance
from map import Map
from object import Object, ObjectId

from collections import defaultdict
from typing import DefaultDict

# type aliasing
InInType = DefaultDict[ObjectId, list[IntersectionInstance]]


class World:
    """Maintains the state of the world including all its objects. There will be
       only one instance of this class, responsible for evolving the objects and
       runs the main cycle.
    
    Attributes:
        objects: dictionary of form [object_id -> Object]
        __creation_ts: timestamp of world creation
        __num_evolutions: how many evolutions have the world had so far
        __duration_sec: determines how many seconds the world instance will exist for
    """
    
    def __init__(self, map_filename: str):
        self.objects: dict[ObjectId, Object] = Map.parse_map(map_filename)
        self.__creation_ts: float = time.time()  # current timestamp
        self.__num_evolutions: int = 0

        # TODO hardcoded parameters here, to be taken care of properly
        self.__duration_sec = 10
                
    def evolve(self, delta_t: float) -> None:
        """Transitions the objects into next state.

        Args:
            delta_t: Time difference between now and next state in seconds.
        """
        for oid in self.objects:
            if self.objects[oid].is_evolvable():
                offspring_objects = self.objects[oid].evolve(delta_t)
                self.add_object(offspring_objects)
                # TODO these newly added objects don't get an evolve() in this round?

        self.delete_expired_objects()

    def add_object(self, new_objects: dict[ObjectId, Object]) -> None:
        """Appends new objects to the list of world objects.

        Args:
            new_objects: Will be added to self.objects
        """
        self.objects.update(new_objects)

    def delete_expired_objects(self) -> None:
        """Removes objects which are supposed to die in this iteration.
        """
        # Cannot erase from dictionary in a loop, so do it in two steps
        delete_keys: list[ObjectId] = []
        for ob in self.objects:
            if ob.time_to_die():
                delete_keys.append(ob)

        for ob in delete_keys:
            del self.objects[ob]

    def intersect(self) -> InInType:
        """Returns the intersection of every pair of objects.

        Returns:
            A dictionary, where a list of IntersectionInstance objects is stored per
            ObjectId
        """
        intersection_result: InInType = defaultdict(list)  # final result
        oids: list[ObjectId] = list(self.objects.keys())  # TODO: better way to get oids?
        for i in range(len(oids)):
            oid_1 = oids[i]
            for j in range(i+1, len(oids)):
                oid_2 = oids[j]
                instance = IntersectionInstance(self.objects[oid_1], self.objects[oid_2])
                # instance has to be added for both objects
                intersection_result[oid_1].append(instance)
                intersection_result[oid_2].append(instance)

        return intersection_result

    def register_intersections(self, intersection_result: InInType) -> None:
        """For each object with intersections, registers the list of its intersections

        Args:
            A dictionary where a list of IntersectionInstance objects is stored per object
        """
        for oid in intersection_result:
            self.objects[oid].set_intersections(intersection_result[oid])
    
    def run(self) -> None:
        """World's main cycle.

        In each iteration, intersections of objects are computed and registered, and then
        each object is evolved.
        """
        # TODO: For now, we will only  run the world for one round
        delta_t_list = [self.__duration_sec+1]
        
        for obj in self.objects:
            delta_t_list.append(obj.get_required_delta_t())
        delta_t = min(set(delta_t_list)-{0})

        # TODO delta_t based on movement of objects, decided by the world, goes here
        
        t = 0
        while t < self.__duration_sec:
            intersection_result = self.intersect()
            self.register_intersections(intersection_result)
            self.evolve(delta_t)
            t = t + delta_t
            self.__num_evolutions += 1
