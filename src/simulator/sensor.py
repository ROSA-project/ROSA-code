from object import Object, ObjectId
from shape import Shape
from position import Position
# from intersection_instance import IntersectionInstance #for the next version


class Sensor(Object):
    # def sense(self, intersections: list[IntersectionInstance]) -> bool #for the next version
    def __init__(self, oid: ObjectId, shape: Shape, position: Position, owner_object: Object):
        super().__init__(oid, shape, position, owner_object)

    def sense(self):
        pass

