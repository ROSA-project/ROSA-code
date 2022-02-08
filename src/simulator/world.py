import time

from intersection_instance import IntersectionInstance
from map import Map
from object import Object, ObjectId

class World:
    """Maintains the state of the world including all its objects. There will be
       only one instance of this class, responsible for evolving the objects and
       runs the main cycle.
    
    Attributes:
        objects: dictionary of form [object_id -> Object]
        delta_t: world evolves every delta_t seconds.
        __creation_ts: timestamp of world creation
        __num_evolutions: how many evolutions have the world had so far
        __duration_sec: determines how many seconds the world instance will exist for
    
    """
    
    def __init__(self, map_filename: str):
        self.objects: dict[ObjectId, Object] = Map.parse_map(map_filename)
        self.__creation_ts: float = time.time()  # current timestamp
        self.__num_evolutions: int = 0

        #TODO hardcoded parameters here, to be taken care of properly
        self.__duration_sec = 10
                
    def evolve(self, delta_t: float) -> None:
        """Transitions the objects into next state.        
        """
        for oid in self.objects:
            if self.objects[oid].is_evolvable():
                offspring_objects = self.objects[oid].evolve(delta_t)
                self.add_object(offspring_objects)
                #TODO these newly added objects don't get an evolve() in this round?

        # time_to_die() of objects has to be checked after the evolve loop. Because collecting the info
        # from the hierarchy of dependent objects is messy.
        for ob in self.objects:
            if ob.time_to_die():
                self.objects.remove(ob)
        #TODO saeed: no idea if this is okay in python :D

    def intersect(self) -> dict[ObjectId, list[IntersectionInstance]]:
        intersection_result = {}
        #TODO currently, some objects could have no intersection (so empty list). room for optimization?
        #TODO decide on structure
        oids: list[ObjectId] = list(self.objects.keys()) # TODO: is there a better way?
        for i in range(len(oids)):
            oid_1 = oids[i]
            intersection_result[oid_1] = []
            for j in range(i+1, len(oids)):
                oid_2 = oids[j]
                instance = IntersectionInstance(self.objects[oid_1], self.objects[oid_2])
                # instance has to be added for both objects
                intersection_result[oid_1].append(instance)
                intersection_result[oid_2].append(instance)

        return intersection_result

    def register_intersections(self, intersection_result: dict[ObjectId, list[IntersectionInstance]]) -> None:
        for oid in self.objects:
            self.objects[oid].set_intersections(intersection_result[oid])
    
    def run(self) -> None:
        #TODO: For now, we will only  run the world for one round
        delta_t_list = [self.__duration_sec+1]
        
        for obj in self.objects:
            delta_t_list.append(obj.get_required_delta_t())
        delta_t = min(set(delta_t_list)-{0})

        #TODO the delta_t based on movement of objects, decided by the world, goes here
        
        t = 0
        while t < self.__duration_sec:
            intersection_result = self.intersect()
            self.register_intersections(intersection_result)
            self.evolve(delta_t)
            t = t + delta_t
            self.__num_evolutions += 1

    def add_object(self, new_objects: list[Object]) -> None:  
        """Appends new objects to the list of world objects.
        """
        self.objects.extend(new_objects)
