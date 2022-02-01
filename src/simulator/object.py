class Object:
    ObjectId = int # type aliasing, since we might change the composition of ObjectId in future
    
    def __init__(self, id: ObjectId, shape: Shape, position: Position):
        self.id = id
        self.shape = shape
        self.position = position
    
    def evolve(self, delta_t: int) -> dict[ObjectId, Object]:
        pass
    
    def visualize(self):
        pass
    
    def bounding_box(self):
        pass
        
        
    