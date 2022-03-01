from position import Position
from shape import Shape
from box import Box

class Cube(Shape):
    def __init__(self, length: float, height: float, width: float):
        self.length = length
        self.height = heitht
        self.width = width
    
    def bounding_box(self, position: Position):
        
        length = cube.length
        height = cube.height
        width = cube.width

        x = position.x
        y = position.y
        z = position.z
        phi = position.phi
        theta = position.theta

        bb_cube = Cube(length, height, width)
        bb_position = Position(x, y, z, phi, theta)

        return Box(bb_cube, bb_position)