from __future__ import annotations
from object import Object, ObjectId
from position import Position
from box import Box
from cube import Cube
from cylinder import Cylinder
from ball import RigidPointBall
from vacuum_cleaner import VacuumCleanerV0
from object_registry import ObjectRegistry
from base import Base
import json


class Map:
    def __init__(self, registry: ObjectRegistry):
        self.next_available_id = 0
        self.registry = registry

    def parse_map(self, filename: str) -> ObjectRegistry:
        """Loads the input json file and creates the objects.
        """
        try:
            with open(filename, "r") as f:
                parsed = json.load(f)
                obj_map = {}
                self.get_objects(obj_map, parsed, None)
                self.registry.add_objects(obj_map)
                return self.registry
        except (OSError, IOError) as e:
            print("Error in opening file ", filename)
            raise e

    def instantiate_object(self, obj_json, new_id: ObjectId, name: string, owner: Object) \
            -> Object:
        shape: Shape = Map.get_shape(obj_json)
        assert (shape is None) == (obj_json["class"] == "CompoundPhysical"), \
            "Only CompoundPhysical objects can be shape-less"
        position: Position = Map.get_position(obj_json)
        cname = obj_json["class"]
        if cname == "Box":
            return Box(new_id, name, shape, position, owner, self.registry)
        elif cname == "RigidPointBall":
            # TODO hardcoding acceleration and velocity not to change 
            # Erfan's code w/o discussion
            # TODO also skipping name for now
            return RigidPointBall(new_id, shape, position, 0, 2, owner, self.registry)
        elif cname == "VacuumCleanerV0":
            bases = obj_json["bases"]
            return VacuumCleanerV0(new_id, name, position, owner, {"diameter": shape.radius, "height": shape.height},
                                   self.registry, bases)
        elif cname == "Base":
            standard_deviation = obj_json["standard_deviation"]
            time_using = obj_json["time_using"]
            return Base(new_id, name, shape, position, owner, self.registry, standard_deviation, time_using)
        else:
            assert cname == "Simple" or cname == "CompoundPhysical", \
                f"Unknown 'class' name for object: {cname}"
            return Object(new_id, name, shape, position, owner, self.registry)

    @staticmethod
    def get_shape(obj_json) -> Shape:
        if "shape" not in obj_json:
            return None
        else:
            try:
                args = obj_json["shape"]["arguments"]
                cname = obj_json["shape"]["class"]
                if cname == "Cube":
                    return Cube(args["length"], args["height"], args["width"])
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

    def get_objects(self, obj_map: dict[ObjectId, Object], parsed, owner: Object) \
            -> dict[ObjectId, Object]:
        # stores a dictionary of objects at this current level (and not deeper)
        this_level_objects = {}
        for oname in parsed:
            new_id: ObjectId = self.registry.get_next_available_id()
            obj = self.instantiate_object(parsed[oname], new_id, oname, owner)
            this_level_objects[new_id] = obj
            if "subobjects" in parsed[oname]:
                assert parsed[oname]["class"] == "CompoundPhysical", \
                    "Only CompoundPhysical objects can have subobjects"
                obj.dependent_objects = self.get_objects(
                    obj_map, parsed[oname]["subobjects"], obj)
            else:
                obj.dependent_objects = {}

            obj_map[new_id] = obj
        return this_level_objects
