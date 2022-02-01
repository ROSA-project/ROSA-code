class World:
    """Maintains the state of the world including all its objects. There will be
       only one instance of this class, responsible for evolving the objects and
       runs the main cycle. 
    """
    def __init__(self, world_map: Map):
        self.objects = {}
        self.__creation_ts
        self.__num_evolutions = 0        
                
    def evolve(self, delta_t: int):
        pass
    
    def intersect(self) -> set[IntersectionInstance]:
        pass
    
    def run(self):
        pass