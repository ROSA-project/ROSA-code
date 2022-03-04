from __future__ import annotations
from position import Position
from shape import Shape
from box import Box

class Cube(Shape):
    def __init__(self, length: float, height: float, width: float):
        self.length = length
        self.height = height
        self.width = width
    
    def bounding_box(position: Position):
        """Returns Box
           Args: position
        """
        
        #dimension calculations                
        length = cube.length
        height = cube.height
        width = cube.width
        
        #position calculations
        x = position.x
        y = position.y
        z = position.z
        phi = position.phi
        theta = position.theta

        #assign return Arguments
        bb_cube = Cube(length, height, width)
        bb_position = Position(x, y, z, phi, theta)

        return Box(bb_cube, bb_position)