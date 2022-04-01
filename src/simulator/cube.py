from shape import Shape
from position import Position

class Cube(Shape):
    def __init__(self, length: float, height: float, width: float):
        self.length = length
        self.height = height
        self.width = width
        self.type = "Cube"
    
    def bounding_box(self,position: Position):
        """Returns a tuple of Cube and Poistion
           # TODO this must be a Box. removed due to circular import issue
           Args: position, coming from the calling Object
        """
        
        #dimension calculations                
        length = self.length
        height = self.height
        width = self.width
        
        #position calculations
        x = position.x
        y = position.y
        z = position.z
        phi = position.phi
        theta = position.theta

        #assign return Arguments
        bb_cube = Cube(length, height, width)
        bb_position = Position(x, y, z, phi, theta)

        # TODO to be replaced with a Box, this is a temp solution for circular 
        # import issue
        return bb_cube, bb_position