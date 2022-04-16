from __future__ import annotations
from object import Object, ObjectId
from position import Position
from box import Box
#from vacuum_cleaner import VacuumCleanerV0


class Map:
    """Handles reading/parsing/loading of the map.
    """

    @staticmethod
    def parse_map(filename: str) -> dict[ObjectId, Object]:
        
        with open(filename, "r") as read_file:
            # parse JSON file
            parsed = json.load(read_file)

        #get objects
        def get_objects(parsed_json, owner: Object) -> dict[ObjectId, Object]:
            output = {}
            for i in parsed_json:
                obj = Object(i, owner)
                if "subobjects" in parsed_json[i]:
                    obj.dependent_objects = get_objects(parsed_json[i]["subobjects"], obj)
                output[i] = obj
    
            return output


        return get_objects(parsed, None)