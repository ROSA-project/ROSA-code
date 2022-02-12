from object import Object


class Robot(Object):
    def __init__(self, id: ObjectId, shape: Shape, position: Position, owner_object):
        # TODO can't type hint owner_object because it doesn't know Object yet :D
        self.id = id
        self.shape = shape
        # shape could be None
        self.position = position
        self.owner_object = owner_object
        self.dependent_objects = []
        super().__init__()
