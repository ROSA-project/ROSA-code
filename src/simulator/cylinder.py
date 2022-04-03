from __future__ import annotations
from position import Position
from shape import Shape
from cube import Cube


class Cylinder(Shape):
    def __init__(self, radius: float, height: float):
        self.radius = radius
        self.height = height
        self.type = "Cylinder"

    def bounding_box(self,position: Position):
        """Returns a tuple of Cube and Poistion
           # TODO this must be a Box. removed due to circular import issue
           Args: position, coming from the calling Object
        """

        #dimension calculations
        length = 2 * self.radius
        height = self.height
        width = 2 * self.radius
        
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