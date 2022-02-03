import intersection_instance
import map
import object

class World:
    """Maintains the state of the world including all its objects. There will be
       only one instance of this class, responsible for evolving the objects and
       runs the main cycle. 
    """
    def __init__(self, world_map: Map):
        self.objects = {}
        self.__creation_ts
        self.__num_evolutions = 0
        
        self.objects = []
        #a list of type Object

        #TODO hardcoded parameters here, to be taken care of properly
        self.total_duration = 10 #in seconds
                
    def evolve(self, delta_t: float):
        for i in range(len(self.objects)):
            if not self.objects[i].owner_object:
                #TODO direct access to object members
                offspring_objects = self.objects[i].evolve(delta_t, self.intersection_result[i])
                self.add_object(offspring_objects)
                #TODO these newly added objects don't get an evolve() in this round?

        # time_to_die() of objects has to be checked after the evolve loop. Because collecting the info
        # from the hierarchy of dependent objects is messy.
        for object in self.objects:
            if object.time_to_die():
                self.objects.remove(object)
        #TODO saeed: no idea if this is okay in python :D

    def intersect(self) -> set[IntersectionInstance]:
        intersection_result = []
        for i in range(len(self.objects)):
            for j in range(len(self.objects)):
                intersection_result[i][j] = IntersectionInstance(self.objects[i],self.objects[j]) 
        
        return intersection_result
    
    def run(self):
        delta_t_list=[]
        for object in self.objects:
            delta_t_list.append(object.get_required_delta_t())
        self.delta_t = min(set(delta_t_list)-{0})

        #TODO the delta_t based on movement of objects, decided by the world, goes here

        if self.delta_t == 0:
            self.delta_t = self.total_duration+1
            #meaning that we need only one round 
            #and the run loop will work only for the initial t.
        
        t = 0
        #TODO t to be initialized if an initial state is given

        while t < self.total_duration:
            self.intersection_result = self.intersect()
            self.evolve(delta_t)
            t = t + self.delta_t

    def add_object(self, new_objects: Object):
        #TODO can we specify a list with these type hints?

        self.objects.extend(new_objects)
