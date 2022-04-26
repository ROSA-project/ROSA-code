from math import dist
from turtle import position
from object import ObjectId, Object
from robot import Robot
from position import Position
from cylinder import Cylinder
from sensor import Sensor
from bumper_sensor import BumperSensor
import numpy as np


class VacuumCleanerV0(Robot):
    def __init__(self, oid: ObjectId, position: Position, owner_object:Object, \
        parameters: dict[str,]):
        # TODO saeed: making assumption that from the usual inputs of Object constructor
        #   we only need position. e.g. robots have no owner? it still doesn't hurt so I
        #   include it.
        # TODO saeed: class-associated object, needs parameters. How do we collect these from
        #   map and pass?
        
        #assuming Robot didn't override Object's constructor
        Robot.__init__(self,oid,\
            Cylinder(parameters["diameter"],parameters["height"]),position, owner_object)
        
        # TODO saeed: where does the oid of sensor comes from? fetched from Map? how do we have
        #  acess to Map here?

        self.sensor: Sensor = BumperSensor(oid,self.shape,position,self)

        self.forward_speed: float = 1 #unit m/s
        self.reverse_speed: float = 0.2
        self.turning_speed: float = 25 #unit deg/s

        self.turn_on_hit_angle: float = 50 #degrees
        self.reverse_on_hit_duration: float = 1 #seconds
        
        #possible states: forward, reverse, turn left
        self.state: str = "forward"
        
        # -1 meaning keep the state unless a hit happnes
        self.state_duration = -1
        self.elapsed_time_on_state=0

        self.total_elapsed_time=0
    
    def evolve(self, delta_t: float) -> dict[ObjectId, Object]:
        if self.sensor.sense(delta_t):
            # a hit occured
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
            #no hit so no unexpcted change of state
            self.elapsed_time_on_state += delta_t
            if self.state_duration != -1:
                # we're in a duration-limited state
                if self.elapsed_time_on_state >= self.state_duration:
                    #time to go back to normal operation of forward
                    self.state = "forward"
                    self.state_duration = -1
                
            if self.state == "forward":
                distance = self.forward_speed * delta_t
                #that is when oriented toward left we get decreasing x
                self.position.x += distance * np.cos(np.pi/180*self.position.phi)
                #that is when oriented toward buttom we get decreasing y
                self.position.y += distance * np.sin(np.pi/180*self.position.phi)
            elif self.state == "turn left":
                # left meaning increasing phi
                rotation = self.turning_speed * delta_t #in degrees
                self.position.phi += rotation 
            elif self.state == "reverse":
                if self.elapsed_time_on_state == 0:
                    #reversing not began yet, reverse the direction
                    self.position.phi = -self.position.phi

                distance = self.reverse_speed * delta_t
                #that is when oriented toward left we get decreasing x
                self.position.x += distance * np.cos(np.pi/180*self.position.phi)
                #that is when oriented toward buttom we get decreasing y
                self.position.y += distance * np.sin(np.pi/180*self.position.phi)
            else:
                raise Exception("unknown state: " + self.state)
        #print("x=" + str(self.position.x) + " ," + "y=" + str(self.position.y) + " ," + \
        #    "phi=" + str(self.position.phi))
        
        self.total_elapsed_time += delta_t
        return dict()

    def get_required_delta_t(self) -> float:
        # say, enough to capture turning or reversing duration in 10 cycles
        delta_t = min(self.turn_on_hit_angle / self.turning_speed, self.reverse_on_hit_duration)/10 
        return delta_t
        

