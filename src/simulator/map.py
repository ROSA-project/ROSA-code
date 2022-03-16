from __future__ import annotations
from object import Object, ObjectId
from cube import Cube
from position import Position
from box import Box

class Map:
    """Handles reading/parsing/loading of the map.
    """

    @staticmethod
    def parse_map(filename: str) -> dict[ObjectId, Object]:
        objects = {}
        # TODO parsing should happen here

        #temporary hardcoding
        cube_0 = Cube(2,3,1)
        cube_1 = Cube(5,1,3)
        position_0 = Position(0,0,0,0,0)
        position_1 = Position(5,3,0,0,0)

        object = {0: Box(cube_0,position_0),
                    1: Box(cube_1,position_1)}

        return objects
