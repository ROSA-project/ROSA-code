from __future__ import annotations

import time
from intersection_instance import IntersectionInstance
from map import Map
from object import Object, ObjectId
from box import Box
from cube import Cube
from position import Position
from object_registry import ObjectRegistry
from collections import defaultdict
from typing import DefaultDict
import json
import saeed_logger as logger

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
        m = Map()
        self.registry: ObjectRegistry = m.parse_map(map_filename)
        # self.objects: dict[ObjectId, Object] = m.parse_map(map_filename)
        self.__vis_data = dict()
        self.__creation_ts: float = time.time()  # current timestamp
        self.__num_evolutions: int = 0
        self.__current_time_ms: int = 0
        self.__vis_output_filename: str = vis_filename
        # TODO hardcoded parameters here, to be taken care of properly
        self.__duration_sec: int = 10
        self.__vis_frame_interval_ms = 0.025
        self.__next_frame_time_msec = 0

    def evolve(self, delta_t: float) -> None:
        """Transitions the objects into next state.

        Args:
            delta_t: Time difference between now and next state in seconds.
        """
        for oid in self.registry.get_objects():
            if self.registry.get_objects()[oid].is_evolvable():
                offspring_objects = self.registry.get_objects()[oid].evolve(delta_t)
                self.registry.add_objects(offspring_objects)
                # TODO these newly added objects don't get an evolve() in this round?

        self.delete_expired_objects()

    def delete_expired_objects(self) -> None:
        """Removes objects which are supposed to die in this iteration.
        """
        # Cannot erase from dictionary in a loop, so do it in two steps
        delete_keys: list[ObjectId] = []
        for oid in self.registry.get_objects():
            if self.registry.get_objects()[oid].time_to_die():
                delete_keys.append(oid)

        for oid in delete_keys:
            del self.registry.get_objects()[oid]

    def intersect(self) -> tuple:
        """Returns the intersection of every pair of objects.

        Returns:
            A dictionary, where a list of IntersectionInstance objects is stored per
            ObjectId
        """
        intersection_result: InInType = defaultdict(list)  # final result
        oids: list[ObjectId] = list(self.registry.get_objects().keys())  # TODO: better way to get oids?
        non_infinitesimal_intersection_exists = False
        for i in range(len(oids)):
            oid_1 = oids[i]
            for j in range(i + 1, len(oids)):
                oid_2 = oids[j]
                # TODO skipping shape-less objects, but shapelessness is not so well-defined
                # let's return to this later
                if not (self.registry.get_objects()[oid_1].shape == None \
                        or self.registry.get_objects()[oid_2].shape == None):
                    instance = IntersectionInstance(self.registry.get_objects()[oid_1],
                                                    self.registry.get_objects()[oid_2])
                    # instance has to be added for both objects
                    intersection_result[oid_1].append(instance)
                    intersection_result[oid_2].append(instance)
                    if instance.does_intersect():
                        if not instance.is_infinitesimal():
                            non_infinitesimal_intersection_exists = True
                        # TODO with the current architecture we could immediately break
                        # and return or throw an exception here. But that would be 
                        # optimization. decide later.

        return intersection_result, non_infinitesimal_intersection_exists

    def register_intersections(self, intersection_result: InInType) -> None:
        """For each object with intersections, registers the list of its intersections

        Args:
            A dictionary where a list of IntersectionInstance objects is stored per object
        """
        for oid in intersection_result:
            self.registry.get_objects()[oid].set_intersections(intersection_result[oid])

    def pick_delta_t(self) -> float:
        """Returns a delta_t for the current cycle
        """
        # TODO: For now, we will only  run the world for one round
        delta_t_list = [self.__duration_sec + 1]
        for oid in self.registry.get_objects():
            delta_t_list.append(self.registry.get_objects()[oid].get_required_delta_t())
        return float(min(set(delta_t_list) - {0}))

    def run(self) -> None:
        """World's main cycle.

        In each iteration, intersections of objects are computed and registered, and then
        each object is evolved.
        """
        non_infinitesimal_intersection_exists: bool = False
        current_percentage = 0
        while self.__current_time_ms < self.__duration_sec:
            delta_t = self.pick_delta_t()
            if int(self.__current_time_ms / self.__duration_sec * 100) > current_percentage:
                current_percentage = int(self.__current_time_ms / self.__duration_sec * 100)
                print(str(current_percentage) + "% processed")
            logger.Logger.add_line("at t = " + str(self.__current_time_ms) + ", "
                                                                             "picked delta_t = " + str(delta_t))
            self.evolve(delta_t)
            intersection_result, non_infinitesimal_intersection_exists = self.intersect()
            # TODO I don't want to assert so I can see the output :D assert kills the wrapper
            # assert(not non_infinitesimal_intersection_exists)
            if non_infinitesimal_intersection_exists:
                print("non-infinitesimal_intersection happened! exiting simulation loop")
                break

            # passes intersection result to the objects
            # where the info will be used by object to handle possible intersection
            # consequences. (differentiate this from object evolution)
            self.register_intersections(intersection_result)

            self.update_visualization_json()

            self.__current_time_ms = self.__current_time_ms + delta_t
            self.__num_evolutions += 1

        self.dump_all_shapes_info()
        self.dump_all_owners_info()
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
        for oid in self.registry.get_objects():
            shapes_info_dict["shapes"][oid] = self.registry.get_objects()[oid].dump_shape_info()
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
        for oid in self.registry.get_objects():
            # TODO:In higher versions, this should be changed (if the visualize method is changed)
            objects_info[oid] = self.registry.get_objects()[oid].visualize()
        return objects_info

    def dump_all_owners_info(self) -> None:
        """ dump visualization info for Owners between objects to the output json file

        """
        owners_info = {"owners": {}}
        for oid in self.registry.get_objects():
            if self.registry.get_objects()[oid].owner_object is not None:
                owners_info["owners"][oid] = str(self.registry.get_objects()[oid].owner_object.oid)
        self.__vis_data.update(owners_info)
