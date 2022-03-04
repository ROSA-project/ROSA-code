from __future__ import annotations
from box import Box
from cube import Cube
from cylinder import Cylinder

def cube_0deg_orientation(cube: Cube) -> bool:
    cube = Cube(2,3,1)
    box = cube.bounding_box(0,0,0)

    if(box.length != 2):
        return False
    if(box.height != 3):
        return False
    if(box.width != 1):
        return False
    if(box.x != 0):
        return False
    if(box.y != 0):
        return False
    if(box.z != 0):
        return False
    if(box.phi != 0):
        return False
    if(box.theta != 0):
        return False

def cylinder_0deg_orientation(cylinder: Cylinder) -> bool:
    cylinder = Cylinder(2,7)
    box = cylinder.bounding_box(0,0,0)

    if(box.length != 4):
        return False
    if(box.height != 7):
        return False
    if(box.width != 4):
        return False
    if(box.x != 0):
        return False
    if(box.y != 0):
        return False
    if(box.z != 0):
        return False
    if(box.phi != 0):
        return False
    if(box.theta != 0):
        return False

def cylinder_90deg_orientation(cylinder: Cylinder) -> bool:
    cylinder = Cylinder(2,7)
    box = cylinder.bounding_box(0,0,0)

    if(box.length != 4):
        return False
    if(box.height != 4):
        return False
    if(box.width != 7):
        return False
    if(box.x != 0):
        return False
    if(box.y != 0):
        return False
    if(box.z != 0):
        return False
    if(box.phi != 0):
        return False
    if(box.theta != 0):
        return False

def main():
        
    test_1 = cube_0deg_orientation()
    assert test_1 ==  "Flase", "Check the Cube with 0 degree Orientation Mode"
    
    test_2 = cylinder_0deg_orientation()
    assert test_2 ==  "Flase", "Check the Cylinder with 0 degree Orientation Mode"
    
    test_3 = cylinder_90deg_orientation()
    assert test_3 ==  "Flase", "Check the Cylinder with 90 degree Orientation Mode"