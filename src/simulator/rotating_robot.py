import object as obj
import robot
import position
import cylinder
import sensor
import distance_measuring_sensor as dms
import bumper_sensor as bs
import object_registry
import numpy as np
import copy


class RotatingRobot(robot.Robot):
    def __init__(self, oid: obj.ObjectId, name: str, pos: position.Position, owner_object: obj.Object,
                 parameters: dict[str,], registry: object_registry.ObjectRegistry):
        robot.Robot.__init__(self, oid, name, cylinder.Cylinder(parameters["diameter"], parameters["height"]),
                             pos, owner_object, registry)
        self.distance_sensor: sensor.Sensor = dms.DistanceMeasuringSensor(self.registry.get_next_available_id(), name,
                                                                          self.shape, pos, self, self.registry)
        shape_cylinder = cylinder.Cylinder(parameters["diameter"]/3, parameters["height"]/3)
        length = parameters["diameter"] + shape_cylinder.height * 0.5
        position_right = copy.copy(pos)
        position_right.theta = 90
        position_right.x = pos.x + length*np.cos(np.deg2rad(position_right.phi))
        position_right.y = pos.y + length*np.sin(np.deg2rad(position_right.phi))
        self.bumper_sensor_right: sensor.Sensor = bs.BumperSensor(self.registry.get_next_available_id(), name,
                                                                  shape_cylinder, position_right, self, self.registry)
        position_up = copy.copy(pos)
        position_up.theta = 90
        position_up.phi = pos.phi + 90
        position_up.x = pos.x + length * np.cos(np.deg2rad(position_up.phi))
        position_up.y = pos.y + length * np.sin(np.deg2rad(position_up.phi))
        self.bumper_sensor_up: sensor.Sensor = bs.BumperSensor(self.registry.get_next_available_id(), name, shape_cylinder
                                                               , position_up, self, self.registry)
        position_down = copy.copy(pos)
        position_down.theta = 90
        position_down.phi = pos.phi + 270
        position_down.x = pos.x + length * np.cos(np.deg2rad(position_down.phi))
        position_down.y = pos.y + length * np.sin(np.deg2rad(position_down.phi))
        self.bumper_sensor_down: sensor.Sensor = bs.BumperSensor(self.registry.get_next_available_id(), name, shape_cylinder
                                                                 , position_down, self, self.registry)
        position_left = copy.copy(pos)
        position_left.theta = 90
        position_left.phi = pos.phi + 180
        position_left.x = pos.x + length * np.cos(np.deg2rad(position_left.phi))
        position_left.y = pos.y + length * np.sin(np.deg2rad(position_left.phi))
        self.bumper_sensor_left: sensor.Sensor = bs.BumperSensor(self.registry.get_next_available_id(), name, shape_cylinder
                                                                 , position_left, self, self.registry)
        self.registry.add_objects({self.distance_sensor.oid: self.distance_sensor})
        self.registry.add_objects({self.bumper_sensor_right.oid: self.bumper_sensor_right})
        self.registry.add_objects({self.bumper_sensor_up.oid: self.bumper_sensor_up})
        self.registry.add_objects({self.bumper_sensor_down.oid: self.bumper_sensor_down})
        self.registry.add_objects({self.bumper_sensor_left.oid: self.bumper_sensor_left})

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


