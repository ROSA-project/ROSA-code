from xmlrpc.client import boolean

from sqlalchemy import false
from simulator.intersection_instance import IntersectionInstance

class Object:
    ObjectId = int # type aliasing, since we might change the composition of ObjectId in future
    
    def __init__(self, id: ObjectId, shape: Shape, position: Position, owner_object: Object):
        self.id = id
        self.shape = shape
        #TODO saeed: isn't shape an inherent property of an object? 
        self.position = position
        self.owner_object = owner_object
        self.dependent_objects = []
    
    def evolve(self, delta_t: int, intersection_result: IntersectionInstance) -> dict[ObjectId, Object]:
        #TODO saeed: could this be the default evolve method?
        collected_offspring_objects = []

        for object in self.dependent_objects:
            offspring_objects = object.evolve(delta_t, intersection_result)
            collected_offspring_objects.extend(offspring_objects)
        
        self.dependent_objects.extend(collected_offspring_objects)
        return collected_offspring_objects
    
    def visualize(self):
        pass
    
    def bounding_box(self):
        pass

    def get_required_delta_t() -> float:
        """returns the delta_t that this object requires to operate right.
           returns 0 if the objects declares no requirement.
        """
        return 0
        
    def time_to_die() -> bool:
        return false