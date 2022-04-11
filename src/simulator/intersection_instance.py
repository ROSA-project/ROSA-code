import object
import numpy as np

class IntersectionInstance:
    """performs intersection between two objects and stores the result. 
       A primary result is a shape.
    """
    def __init__(self, object1: object.Object, object2: object.Object):
        self.object1 = object1
        self.object2 = object2
        self.__does_intersect = False
        self.__is_infinitestimal = False
        self.intersect()

    def intersect(self) -> dict:
        """ performs the intersection algorithm on its two objects, and returns what?!

        Returns:
            not clear for now, as it's not clear what information we need.
            Returns None if no intersection.
        """
        # TODO a temporary implementation for pairs of supported geometrical shapes
        shape_classes = []
        shape_classes.append((self.object1.shape.dump_info())["type"])
        shape_classes.append((self.object2.shape.dump_info())["type"])

        if "Cylinder" in shape_classes and "Cube" in shape_classes:
            self.cylinder_cube()
        elif shape_classes == ["Cube","Cube"]:
            self.cube_cube()
        else:
            raise Exception("Cannot intersect the given objectIDs " + \
                str(self.object1.oid) + " and " + str(self.object2.oid))
    
    def does_intersect(self) -> bool:
        return self.__does_intersect

    def cylinder_cube(self):
        # TODO assuming objects with theta=0, i.e upright
        # and intersecting 2D
        
        if (self.object1.shape.dump_info())["type"] == "Cylinder":
            cylinder_object = self.object1
            cube_object = self.object2
        else:
            cylinder_object = self.object2
            cube_object = self.object1
        
        circle_radius = cylinder_object.shape.radius
        circle_center = [cylinder_object.position.x , cylinder_object.position.y]

        # TODO in our code length and width are not well defined but visaulization
        # is taking width as y-axis-side and so on. import for the input to the
        # followunng function
        rectangle_length = cube_object.shape.length
        rectangle_width = cube_object.shape.width
        rectangle_center = [cube_object.position.x , cube_object.position.y]
        rectangle_phi = cube_object.position.phi
    
        #find the 4 lines of the cube(recatngle) and run line-circle intersections
        lines = self.rectangle_lines(rectangle_center, rectangle_length, rectangle_width,\
                                rectangle_phi)
        
        for line in lines:
            intersection_points_distance = self.line_circle(line[0],line[1], \
                circle_center, circle_radius)
            if intersection_points_distance >= 0:
                self.__does_intersect = True
                print("intersection happened")
                if intersection_points_distance > 0.1:
                    self.__is_infinitestimal = False
                else:
                    self.__is_infinitestimal = True
        

    def line_circle(self, p1, p2, circle_center, circle_radius):
        if p1[0] == p2[0]:
            #vertical line
            intersect_points_distance = -1
            # if abs(p1[0] - circle_center[0]) > circle_radius or \
            #     min(p1[1],p2[1]) > (circle_center[1] + circle_radius) or \
            #     max(p1[1],p2[1]) < (circle_center[1] - circle_radius) :
            #     #not intersecting
            #     intersect_points_distance = -1
            # elif abs(p1[0] - circle_center[0]) == circle_radius:
            #     #intersecting at perimeter
            #     intersect_points_distance = 0
            # else:
            #     intersect_points_distance = 
        else:
            m = (p2[1] - p1[1])/(p2[0]-p1[0]) #slope
            print("slope is " + str(m))
            h = p1[1] - m * p1[0]
            a = 1 + m**2
            b = 2*m*h - 2*m*circle_center[1] -2*circle_center[0]
            c = circle_center[0]**2 + h**2 + circle_center[1]**2 -2*h*circle_center[1] \
                - circle_radius**2
            delta = b**2 - 4*a*c
            if delta < 0 :
                #no solution
                intersect_points_distance = -1
            else:
                #two distinct or not solutions
                #x1 < x2
                x1=(-b - np.sqrt(delta))/(2*a)
                x2=(-b + np.sqrt(delta))/(2*a)
                y1=m*x1+h
                y2=m*x2+h
                if (x1 < p1[0] and x2 < p2[0]) or \
                    (x1 > p2[0] and x2 > p2[0]):
                    #no intersection
                    intersect_points_distance = -1
                #elif (x1 < p1[0] and p1[0] < x2) or \
                #    (x1 < p2[0] and p2[0] < x2):
                # TODO cover above condition
                else:
                    intersect_points_distance = np.sqrt((y2-y1)**2 + (x2-x1)**2)

        return intersect_points_distance

    def rectangle_lines(self, center: list[float], x_axis_side: float, \
                            y_axis_side: float, phi: float):
        # TODO assuming that cube position is at its center
        x=center[0]
        y=center[1]
        points=[]
        points.append([-x_axis_side/2, -y_axis_side/2])
        points.append([+x_axis_side/2, -y_axis_side/2])
        points.append([+x_axis_side/2, +y_axis_side/2])
        points.append([-x_axis_side/2, +y_axis_side/2])
        #now rotate by phi
        R = np.array([[np.cos(phi), -np.sin(phi)],[np.sin(phi), np.cos(phi)]])
        points = R.dot((np.array(points)).T).T
        points = points + np.array(center)
        lines = []
        lines.append([points[0],points[1]])
        lines.append([points[1],points[2]])
        lines.append([points[2],points[3]])
        lines.append([points[3],points[0]])
        return lines

    def cube_cube(self):        
        pass

    def is_infinitesimal(self) -> bool:
        return self.__is_infinitestimal

    