from cube import Cube
from position import Position

class Box(Object):
    def __init__(self, cube: Cube, position: Position):
        self.cube = cube
        self.position = position
