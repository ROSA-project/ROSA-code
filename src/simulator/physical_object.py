from object import Object, ObjectId
import shape
import position
import numpy as np


class RigidPhysicalObject(Object):
    """
    A general rigid physical object, i.e. does not change shape by assumption,
    and is evolved as if it is a point with no shape. Hence, e.g. no rotation.
    The object has acceleration and velocity in addition to the position.
    """

    def __init__(self, oid: ObjectId, shape: shape.Shape, 
                 position: position.Position, acceleration: float, 
                 velocity: float, owner_object: Object):
        
        Object.__init__(self,oid, shape, position, owner_object)
        self.acceleration: float = acceleration
        self.velocity: float = velocity
        print(self._infinitesimal_intersection_occured)

    def evolve(self, delta_t: float):
        if self._infinitesimal_intersection_occured:
            #this is a bump which affects object's movement in this cycle
            self.update_state_upon_bump()
        r = self.velocity * delta_t
        self.position.x += r * np.cos(self.position.phi)
        self.position.y += r * np.sin(self.position.phi)
        return {}
    
    def update_state_upon_bump(self):
        """
        calculates the new motion state
        """
        pass

        

