import time

from intersection_instance import IntersectionInstance
from map import Map
from object import Object

class World:
    """Maintains the state of the world including all its objects. There will be
       only one instance of this class, responsible for evolving the objects and
       runs the main cycle.
    
    Attributes:
        objects: a list of Objects
        delta_t: world evolves every delta_t seconds.
        __creation_ts: timestamp of world creation
        __num_evolutions: how many evolutions have the world had so far
        __duration_sec: determines how many seconds the world instance will exist for
    
    """
    
    def __init__(self, world_map: Map):        
        self.__creation_ts = time.time() # current timestmap
        self.__num_evolutions = 0
        self.objects: list[Object] = []

        #TODO hardcoded parameters here, to be taken care of properly
        self.__duration_sec = 10
            
                
    def evolve(self, delta_t: float) -> None:
        """Transitions the objects into next state.        
        """
        for i in range(len(self.objects)):
            if not self.objects[i].owner_object:
                #TODO direct access to object members
                offspring_objects = self.objects[i].evolve(delta_t, self.intersection_result[i])
                self.add_object(offspring_objects)
                #TODO these newly added objects don't get an evolve() in this round?

        # time_to_die() of objects has to be checked after the evolve loop. Because collecting the info
        # from the hierarchy of dependent objects is messy.
        for object in self.objects:
            if object.time_to_die():
                self.objects.remove(object)
        #TODO saeed: no idea if this is okay in python :D

    def intersect(self) -> set[IntersectionInstance]:
        intersection_result = []
        #TODO decide on structure
        
        for i in range(len(self.objects)):
            for j in range(len(self.objects)):
                intersection_result.append(IntersectionInstance(self.objects[i],self.objects[j]))
        
        return intersection_result
    
    def run(self) -> None:
        #TODO: For now, we will only  run the world for one round
        delta_t_list=[self.__duration_sec+1]
        
        for object in self.objects:
            delta_t_list.append(object.get_required_delta_t())
        self.delta_t = min(set(delta_t_list)-{0})

        #TODO the delta_t based on movement of objects, decided by the world, goes here
        
        t = 0
        while t < self.__duration_sec:
            self.intersection_result = self.intersect()
            self.evolve(delta_t)
            t = t + self.delta_t
            self.__num_evolutions += 1

    def add_object(self, new_objects: list[Object]) -> None:  
        """Appends new objects to the list of world objects.
        """
        self.objects.extend(new_objects)