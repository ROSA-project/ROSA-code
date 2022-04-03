from __future__ import annotations
from object import Object, ObjectId
from cube import Cube
from position import Position
from box import Box
from vacuum_cleaner import VacuumCleanerV0

class Map:
    """Handles reading/parsing/loading of the map.
    """

    @staticmethod
    def parse_map(filename: str) -> dict[ObjectId, Object]:
        objects = {}
        # TODO parsing should happen here

        #temporary hardcoding
        
        box0=Box(0, Cube(2,3,1),Position(0,0,0,0,0),None)
        #box1=Box(1, Cube(5,1,3),Position(5,3,0,0,0),None)
        #box2=Box(2, Cube(1,1,1),Position(2,2,0,0,0),box1)
        
        #objects = {0: box0, 1: box1, 2: box2}
        vacuum_cleaner_0=VacuumCleanerV0(0,Position(0,0,0,0,0),None,{"diameter":0.4,"height":0.1})
        vacuum_cleaner_1=VacuumCleanerV0(0,Position(4,4,0,90,0),None,{"diameter":1,"height":0.1})
        objects={0: box0, 1:vacuum_cleaner_0, 2:vacuum_cleaner_1}

        return objects
