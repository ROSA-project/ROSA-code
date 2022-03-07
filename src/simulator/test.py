from __future__ import annotations
from bumper_sensor import BumperSensor
from robot import Robot

bar = Robot(0, 0, 0, 0, 0)


for i in range(20):
    bar = Robot(bar.evolve(BumperSensor.sense(0))[0], bar.evolve(BumperSensor.sense(0))[1],
                bar.evolve(BumperSensor.sense(0))[2], bar.evolve(BumperSensor.sense(0))[3],
                bar.evolve(BumperSensor.sense(0))[4])
    print(bar.evolve(BumperSensor.sense(0)))

