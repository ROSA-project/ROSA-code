import object
import shape
import position
import numpy as np
import copy
import logger


class RigidPhysicalObject(object.Object):
    """
    A general rigid physical object, i.e. does not change shape by assumption,
    and is evolved as if it is a point with no shape. Hence, e.g. no rotation.
    The object has acceleration and velocity in addition to the position.
    """

    def __init__(self, oid: object.ObjectId, shape: shape.Shape,
                 position: position.Position, acceleration: float, 
                 velocity: float, owner_object: object.Object):
        
        object.Object.__init__(self,oid, shape, position, owner_object)
        self.acceleration: float = acceleration
        self.velocity: float = velocity

    def evolve(self, delta_t: float):
        if self._infinitesimal_intersection_occured:
            #this is a bump which affects object's movement in this cycle
            logger.Logger.add_line("RigidPhysicalObject infinitestimal intersection, redirecting to update_state_upon_bump")
            new_position = self.new_position_upon_bump()
        else:
            new_position = copy.copy(self.position)

        r = self.velocity * delta_t
        new_position.x += r * np.cos(new_position.phi * np.pi/180)
        new_position.y += r * np.sin(new_position.phi * np.pi/180)
        self.update_position(new_position)
        
        offspring_objects = {}
        return offspring_objects
    
    def new_position_upon_bump(self):
        """
        calculates the new motion state
        """
        pass

        

