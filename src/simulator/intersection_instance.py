from object import Object
from shape import Shape, VoidShape


class IntersectionInstance:
    """performs intersection between two objects and stores the result. 
       A primary result is a shape.
    """
    def __init__(self, object1: Object, object2: Object):
        self.object1 = object1
        self.object2 = object2
        self.result = self.intersect()

    def intersect(self) -> Shape:
        """ performs the intersection algorithm on objects: self.object1 and object2
        """
        #TODO to be implemented, this is a placeholder
        return VoidShape()

    