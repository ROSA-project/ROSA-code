import intersection_instance
import map
import parameters as params

class World:
    """Maintains the state of the world including all its objects. There will be
       only one instance of this class, responsible for evolving the objects and
       runs the main cycle. 
    """
    def __init__(self, world_map: Map):
        self.objects = {}
        self.__creation_ts
        self.__num_evolutions = 0
        
        self.objects
        #a list of type Object
                
    def evolve(self, delta_t: float):
        for i in range(len(self.objects)):
            offspring_objects=self.objects[i].evolve(delta_t, self.intersectionResult[i])
            self.addObject(offspring_objects)
    
    def intersect(self) -> set[IntersectionInstance]:
        # for every object i:
        # for every other object j:
        #     if not cubesIntersect(objects[i].boundingBox()
        #             ,objects[j].boundingBox()):
        #         intersectionResult[i]=empty
        #     else:
        #         intersectionResult[i][j]=no idea what to do, an instance of InIn 
        #         #they still might have no intersection. 
        #         #But if they do we need some details
        pass
    
    def run(self):
        t=0
        #TODO t to be initialized if an initial state is given

        delta_t_list=[]
        for object in self.Objects:
            delta_t_list.append(object.get_required_delta_t())
        delta_t=min(delta_t_list)
        
        while t < params.total_duration:
            intersectionResult=self.intersect()
            self.evolve(intersectionResult)
            t=t+delta_t