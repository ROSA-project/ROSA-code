from turtle import position
from position import Position
from world import World
from map import Map
from object import Object
from shape import Shape
from position import Position

class TestWorld(World):
    def __init__(self, world_map: Map):
        super().__init__(world_map)
        object1=Object(0,Shape(),Position(0,0,0,0,0),None)
        object2=Object(1,Shape(),Position(0,0,0,0,0),None)
        object3=Object(1,Shape(),Position(0,0,0,0,0),object2)
        
        self.objects.append(object1)
        self.objects.append(object2)

my_map=Map()
my_world=TestWorld(my_map)
my_world.run()