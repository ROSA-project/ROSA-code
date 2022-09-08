from math import dist
import object
from robot import Robot
from position import Position
from cylinder import Cylinder
from sensor import Sensor
from bumper_sensor import BumperSensor
from object_registry import ObjectRegistry
import numpy as np
import copy
import base


class VacuumCleanerV0(Robot):
    def __init__(self, oid: object.ObjectId, name: str, position: Position, owner_object: object.Object, \
                 parameters: dict[str,], registry: ObjectRegistry):
        # TODO saeed: making assumption that from the usual inputs of Object constructor
        #   we only need position. e.g. robots have no owner? it still doesn't hurt so I
        #   include it.
        # TODO saeed: class-associated object, needs parameters. How do we collect these from
        #   map and pass?
        # assuming Robot didn't override Object's constructor
        Robot.__init__(self, oid, name, \
                       Cylinder(parameters["diameter"], parameters["height"]), position, owner_object, registry)
        # TODO saeed: where does the oid of sensor comes from? fetched from Map? how do we have
        #  acess to Map here?
        self.sensor: Sensor = BumperSensor(self.registry.get_next_available_id(), name, self.shape, position, self,
                                           self.registry)
        self.registry.add_objects({self.sensor.oid: self.sensor})

        self.forward_speed: float = 1  # unit m/s
        self.reverse_speed: float = 0.2
        self.turning_speed: float = 50  # unit deg/s

        self.turn_on_hit_angle: float = 50  # degrees
        self.reverse_on_hit_duration: float = 1  # seconds

        # possible states: forward, reverse, turn left
        self.state: str = "forward"

        # -1 meaning keep the state unless a hit happnes
        self.state_duration = -1
        self.elapsed_time_on_state = 0

        self.total_elapsed_time = 0
        self.bases = dict()

    def evolve(self, delta_t: float) -> dict[object.ObjectId, object.Object]:
        if self.sensor.sense():
            # a hit occured.
            # State (position) is reverted by Object. Here we just make a decision
            # about what to do upon bump
            self.elapsed_time_on_state = 0
            if self.state == "forward":
                self.state = "turn left"
                self.state_duration = self.turn_on_hit_angle / self.turning_speed
            elif self.state == "turn left":
                self.state = "reverse"
                self.state_duration = self.reverse_on_hit_duration
            elif self.state == "reverse":
                self.state = "turn left"
                self.state_duration = self.turn_on_hit_angle / self.turning_speed
            else:
                raise Exception("unknown state: " + self.state)
        else:
            # no hit so no unexpcted change of state
            self.elapsed_time_on_state += delta_t
            new_position = copy.copy(self.position)
            if self.state_duration != -1:
                # we're in a duration-limited state
                if self.elapsed_time_on_state >= self.state_duration:
                    # time to go back to normal operation of forward
                    self.state = "forward"
                    self.state_duration = -1

            if self.state == "forward":
                distance = self.forward_speed * delta_t
                # that is when oriented toward left we get decreasing x
                new_position.x += distance * np.cos(np.pi / 180 * self.position.phi)
                # that is when oriented toward buttom we get decreasing y
                new_position.y += distance * np.sin(np.pi / 180 * self.position.phi)
            elif self.state == "turn left":
                # left meaning increasing phi
                rotation = self.turning_speed * delta_t  # in degrees
                new_position.phi += rotation
            elif self.state == "reverse":
                if self.elapsed_time_on_state == 0:
                    # reversing not began yet, reverse the direction
                    new_position.phi = -self.position.phi

                distance = self.reverse_speed * delta_t
                # that is when oriented toward left we get decreasing x
                new_position.x += distance * np.cos(np.pi / 180 * self.position.phi)
                # that is when oriented toward buttom we get decreasing y
                new_position.y += distance * np.sin(np.pi / 180 * self.position.phi)
            else:
                raise Exception("unknown state: " + self.state)

            self.update_position(new_position)
            self.sensor.update_position(new_position)

        # print("x=" + str(self.position.x) + " ," + "y=" + str(self.position.y) + " ," + \
        #    "phi=" + str(self.position.phi))

        self.total_elapsed_time += delta_t
        return dict()

    def get_required_delta_t(self) -> float:
        # say, enough to capture turning or reversing duration in 10 cycles
        delta_t = min(self.turn_on_hit_angle / self.turning_speed, self.reverse_on_hit_duration) / 10
        return delta_t

    def get_base(self, b: base.Base):
        self.bases[b.oid] = b

    def get_distance_from_base(self, oid: object.ObjectId) -> float:
        """
        robot get distance between self and base
        """
        if oid in self.bases:
            return self.bases[oid].get_distance(self.position)
        else:
            raise Exception("Error! ID Not found.")
