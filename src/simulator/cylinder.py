from position import Position
from shape import Shape
from cube import Cube
from box import Box

class Cylinder(Shape):
    def __init__(self, radius, height):
        self.radius = radius
        self.height = height

    def bounding_box(self, cube: Cube, position: Position) ->Box:
        
        length = 2 * cylinder.radius
        height = cylinder.height
        width = 2 * cylinder.radius
        
        x = position.x
        y = position.y
        z = position.z
        phi = position.phi
        theta = position.theta

        bb_cube = Cube(length, height, width)        
        bb_position = Position(x, y, z, phi, theta)

        return Box(bb_cube, bb_position)