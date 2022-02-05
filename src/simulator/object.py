#from xmlrpc.client import boolean
#from sqlalchemy import false

# postponed evaluation of annotations. With python 3.11, we won't need this
from __future__ import annotations
from shape import Shape
from position import Position

ObjectId = int # type aliasing, since we might change the composition of ObjectId in future

class Object:
    def __init__(self, id: ObjectId, shape: Shape, position: Position, owner_object):
        #TODO can't type hint owner_object because it doesn't know Object yet :D
        self.id = id
        self.shape = shape
        #shape could be None
        self.position = position
        self.owner_object = owner_object
        self.dependent_objects = []
    
    def evolve(self, delta_t: int, intersection_result ) -> dict[ObjectId, Object]:
        #TODO type of intersection rejsult
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

    def get_required_delta_t(self) -> float:
        """returns the delta_t that this object requires to operate right.
           returns 0 if the objects declares no requirement.
        """
        return 0
        
    def time_to_die(self) -> bool:
        return False