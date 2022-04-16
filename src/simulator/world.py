from __future__ import annotations

import time

from intersection_instance import IntersectionInstance
from map import Map
from object import Object, ObjectId
from box import Box
from cube import Cube
from position import Position

from collections import defaultdict
from typing import DefaultDict

import json
# type aliasing
InInType = DefaultDict[ObjectId, list[IntersectionInstance]]


class World:
    """Maintains the state of the world including all its objects. There will be
       only one instance of this class, responsible for evolving the objects and
       runs the main cycle.
    
    Attributes:
        objects: dictionary of form [object_id -> Object]
        __creation_ts: timestamp of world creation
        __num_evolutions: how many evolutions have the world had so far
        __duration_sec: determines how many seconds the world instance will exist for
        __vis_data: a dictionary containing
        __vis_output_filename: the name of file for information
        __current_time_msec: simulator's current time in millisecond
        __vis_frame_interval_msec: the time in msec between each two visualization frames
        __next_frame_time_msec: the time in which the next frame will be taken
    """

    def __init__(self, map_filename: str, vis_filename: str):
        self.objects: dict[ObjectId, Object] = Map.parse_map(sample_room.json)
        self.__vis_data = dict()
        self.__creation_ts: float = time.time()  # current timestamp
        self.__num_evolutions: int = 0
        self.__current_time_ms: int = 0
        self.__vis_output_filename: str = vis_filename
        # TODO hardcoded parameters here, to be taken care of properly
        self.__duration_sec: int = 20
        self.__vis_frame_interval_ms = 0.025
        self.__next_frame_time_msec = 0
                
    def evolve(self, delta_t: float) -> None:
        """Transitions the objects into next state.

        Args:
            delta_t: Time difference between now and next state in seconds.
        """
        for oid in self.objects:
            if self.objects[oid].is_evolvable():
                offspring_objects = self.objects[oid].evolve(delta_t)
                self.add_object(offspring_objects)
                # TODO these newly added objects don't get an evolve() in this round?

        self.delete_expired_objects()

    def add_object(self, new_objects: dict[ObjectId, Object]) -> None:
        """Appends new objects to the list of world objects.

        Args:
            new_objects: Will be added to self.objects
        """
        self.objects.update(new_objects)

    def delete_expired_objects(self) -> None:
        """Removes objects which are supposed to die in this iteration.
        """
        # Cannot erase from dictionary in a loop, so do it in two steps
        delete_keys: list[ObjectId] = []
        for oid in self.objects:
            if self.objects[oid].time_to_die():
                delete_keys.append(oid)

        for oid in delete_keys:
            del self.objects[oid]

    def intersect(self) -> InInType:
        """Returns the intersection of every pair of objects.

        Returns:
            A dictionary, where a list of IntersectionInstance objects is stored per
            ObjectId
        """
        intersection_result: InInType = defaultdict(list)  # final result
        oids: list[ObjectId] = list(self.objects.keys())  # TODO: better way to get oids?
        for i in range(len(oids)):
            oid_1 = oids[i]
            for j in range(i+1, len(oids)):
                oid_2 = oids[j]
                instance = IntersectionInstance(self.objects[oid_1], self.objects[oid_2])
                # instance has to be added for both objects
                intersection_result[oid_1].append(instance)
                intersection_result[oid_2].append(instance)

        return intersection_result

    def register_intersections(self, intersection_result: InInType) -> None:
        """For each object with intersections, registers the list of its intersections

        Args:
            A dictionary where a list of IntersectionInstance objects is stored per object
        """
        for oid in intersection_result:
            self.objects[oid].set_intersections(intersection_result[oid])

    def pick_delta_t(self) -> float:
        """Returns a delta_t for the current cycle
        """
        # TODO: For now, we will only  run the world for one round
        delta_t_list = [self.__duration_sec + 1]
        for oid in self.objects:
            delta_t_list.append(self.objects[oid].get_required_delta_t())
        return float(min(set(delta_t_list) - {0}))

    def run(self) -> None:
        """World's main cycle.

        In each iteration, intersections of objects are computed and registered, and then
        each object is evolved.
        """
        delta_t = self.pick_delta_t()
        while self.__current_time_ms < self.__duration_sec:
            intersection_result = self.intersect()
            self.register_intersections(intersection_result)
            self.update_visualization_json()
            self.evolve(delta_t)
            self.__current_time_ms = self.__current_time_ms + delta_t
            self.__num_evolutions += 1

        self.dump_all_shapes_info()
        self.dump_vis_data_to_file()

    def update_visualization_json(self):
        step_round = 3
        while self.__current_time_ms >= self.__next_frame_time_msec:
            key = ("{:." + str(step_round) + "f}").format(self.__next_frame_time_msec)
            self.__vis_data[key] = self.visualize()
            self.__next_frame_time_msec += self.__vis_frame_interval_ms

    def dump_all_shapes_info(self):
        # dump visualization info for shapes to the output json file
        shapes_info_dict = {"shapes": {}}
        for oid in self.objects:
            shapes_info_dict["shapes"][oid] = self.objects[oid].dump_shape_info()

        self.__vis_data.update(shapes_info_dict)

    def dump_vis_data_to_file(self):
        try:
            with open(self.__vis_output_filename, "w") as json_file:
                json.dump(self.__vis_data, json_file, indent=2)
        except (OSError, IOError) as e:
            print("Error in writing to file ", self.__vis_output_filename)
            raise e

    def visualize(self) -> dict:
        """Sets position of the objects with moment (time)
        
        Returns:
            Dictionary with ObjectID as key, and object's visualization info as value.
        """
        objects_info = dict()
        for oid in self.objects:
            objects_info[oid] = self.objects[oid].visualize()
        return objects_info
