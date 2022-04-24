from __future__ import annotations
from object import Object, ObjectId
from position import Position
from box import Box
from cube import Cube
from cylinder import Cylinder
import json


class Map:
    def __init__(self):
        self.next_available_id = 0

    def parse_map(self, filename: str) -> dict[ObjectId, Object]:
        """Loads the input json file and creates the objects.
        """
        try:
            with open(filename, "r") as f:
                parsed = json.load(f)
                return self.get_objects(parsed, None)
        except (OSError, IOError) as e:
            print("Error in opening file ", filename)
            raise e

    def get_next_id(self) -> ObjectId:
        oid = self.next_available_id
        self.next_available_id += 1
        return oid

    @staticmethod
    def instantiate_object(obj_json, new_id: ObjectId, name: string, owner: Object)\
            -> Object:
        shape: Shape = Map.get_shape(obj_json)
        position: Position = Map.get_position(obj_json)
        cname = obj_json["class"]
        if cname == "Box":
            return Box(new_id, name, shape, position, owner)
        else:
            return Object(new_id, name, shape, position, owner)

    @staticmethod
    def get_shape(obj_json) -> Shape:
        if "shape" not in obj_json:
            return None
        else:
            try:
                args = obj_json["shape"]["arguments"]
                cname = obj_json["shape"]["class"]
                if cname == "Cube":
                    return Cube(args["lenght"], args["height"], args["width"])
                elif cname == "Cylinder":
                    return Cylinder(args["radius"], args["height"])
                else:
                    raise ValueError("Unknown shape: ", cname)
            except Exception as e:
                print("Error in parsing object's shape: ", str(e))
                raise e

    @staticmethod
    def get_position(obj_json) -> Shape:
        try:
            p = obj_json["position"]
            return Position(p[0], p[1], p[2], p[3], p[4])
        except Exception as e:
            print("Error in parsing object's position: ", str(e))
            raise e

    def get_objects(self, parsed, owner: Object) -> dict[ObjectId, Object]:
        output = {}
        for oname in parsed:
            new_id: ObjectId = self.get_next_id()
            obj = self.instantiate_object(parsed[oname], new_id, oname, owner)
            if "subobjects" in parsed[oname]:
                obj.dependent_objects = self.get_objects(parsed[oname]["subobjects"], obj)
            output[new_id] = obj
        return output


