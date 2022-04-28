from __future__ import annotations
import logger
import object
import numpy as np

# TODO move
epsilon_criterion = 0.1
non_zero_criterion = 0.0001

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
        # is taking width as y-axis-side and so on. important for the input to the
        # following function
        rectangle_length = cube_object.shape.length
        rectangle_width = cube_object.shape.width
        rectangle_center = [cube_object.position.x , cube_object.position.y]
        rectangle_phi_rad = cube_object.position.phi * np.pi/180
    
        #find the 4 lines of the cube(recatngle) and run line-circle intersections
        lines = IntersectionInstance.rectangle_lines(rectangle_center, \
            rectangle_length, rectangle_width, rectangle_phi_rad)
        
        intersection_points_distance = []
        for line in lines:
            intersection_points_distance.append(self.line_circle(line[0],line[1], \
                circle_center, circle_radius))
        
        # TODO strictly larger than 0 must be documented. see calculation of the distance
        if max(intersection_points_distance) > non_zero_criterion:
            self.__does_intersect = True
            if max(intersection_points_distance) > epsilon_criterion:
                self.__is_infinitestimal = False
            else:
                self.__is_infinitestimal = True
        

    def line_circle(self, p1, p2, circle_center, circle_radius):
        """
        Calculates the intersection of a line segment and a circle.
        inputs:
            p1,p2: start and end point of the line segment, each a list
                   with first element as x and second as y of the point
            circle_center: an x-y point as defined for p1 and p2
            circle_radius: clear
        output:
            consider the infinite line on which the line segment lies
            and consider points i1 and i2 at which the circle intersects with
            the infinite line.
            the return value is the distance of the intersection of two line segments
            p1-p2 and i1-i2.
        """
        if p1[0] == p2[0]:
            phi_rad = np.pi/2
        else:
            #m = (p2[1] - p1[1]) / (p2[0]-p1[0]) #slope
            # TODO arc
            phi_rad = np.arctan2((p2[1] - p1[1]),(p2[0]-p1[0]))
        
        r_matrix=IntersectionInstance.rotation_matrix_2d(-phi_rad)

        logger.Logger.add_line("line-circle intersection:")
        logger.Logger.add_line("input line = " + str(p1) + " , " + str(p2))
        logger.Logger.add_line("input circle center = " + str(circle_center) + " and radius = " + str(circle_radius))

        p1 = r_matrix.dot(p1)
        p2 = r_matrix.dot(p2)
        circle_center = r_matrix.dot(circle_center)
       
        logger.Logger.add_line("rotated line =" + str(p1) + " , " + str(p2))
        logger.Logger.add_line("rotated circle center " + str(circle_center))

        if p1[1] < circle_center[1] - circle_radius or \
                p1[1] > circle_center[1] + circle_radius:
            #vertically seperated
            #logger.Logger.add_line("vertically seperated")
            intersect_points_distance = -1
        elif np.linalg.norm(self.horizontal_line_segment_intersection(p1,p2,
                [circle_center[0]-circle_radius, circle_center[1]],
                [circle_center[0]+circle_radius, circle_center[1]])) == 0:
            #horizontally separated
            #logger.Logger.add_line("horizontally seperated")
            intersect_points_distance = -1
        else:
            #logger.Logger.add_line("need to calculate the intersection")
            m = 0 
            h = p1[1] - m * p1[0]
            a = 1 + m**2
            b = 2*m*h - 2*m*circle_center[1] -2*circle_center[0]
            c = circle_center[0]**2 + h**2 + circle_center[1]**2 -2*h*circle_center[1] \
                - circle_radius**2
            delta = b**2 - 4*a*c
            if delta < 0 :
                #no solution
                intersect_points_distance = -1
                logger.Logger.add_line("delta < 0")
            else:
                #two distinct or equal solutions
                #x1 < x2
                x1=(-b - np.sqrt(delta))/(2*a)
                x2=(-b + np.sqrt(delta))/(2*a)
                y1=m*x1+h
                y2=m*x2+h
                x_intersect_points=self.horizontal_line_segment_intersection(\
                    [x1,y1],[x2,y2],p1,p2)
                # undo the rotation
                r_inv_matrix=IntersectionInstance.rotation_matrix_2d(phi_rad)
                tmp =  r_inv_matrix.dot(\
                    [np.mean(x_intersect_points),p1[1]])
                # TODO adding zero as the z
                # TODO turning this into numpy array because get_intersection_point
                #  retunr value should be so
                self._intersection_point = np.array([tmp[0],tmp[1],0])
                
                intersect_points_distance = abs(x_intersect_points[0]-x_intersect_points[1])
                
       
        logger.Logger.add_line("oid's " + str(self.object1.oid) + " , " + \
            str(self.object2.oid) + ": intersection points distance = " \
                +str(intersect_points_distance))
        return intersect_points_distance

    def rectangle_lines(center: list[float], x_axis_side: float, \
                            y_axis_side: float, phi_rad: float):
        """
            return values is a numpy array, a matrix of vectors each being a line
        """
        # TODO assuming that cube position is at its center
        points=[]
        points.append([-x_axis_side/2, -y_axis_side/2])
        points.append([+x_axis_side/2, -y_axis_side/2])
        points.append([+x_axis_side/2, +y_axis_side/2])
        points.append([-x_axis_side/2, +y_axis_side/2])
        #now rotate by phi
        r_matrix=IntersectionInstance.rotation_matrix_2d(phi_rad)
        points = r_matrix.dot((np.array(points)).T).T
        points = points + np.array(center)
        lines = []
        lines.append([points[0],points[1]])
        lines.append([points[1],points[2]])
        lines.append([points[2],points[3]])
        lines.append([points[3],points[0]])
        logger.Logger.add_line("For the rectangle with center at " + str(center) + ", x_side = " + \
            str(x_axis_side) + ", y_axis = " + str(y_axis_side) + ", the points are:")
        logger.Logger.add_line(str(lines))
        return lines

    def rotation_matrix_2d(phi: float):
        """
        phi in radians
        [ cos(phi)  -sin(phi)
          sin(phi)   cos(phi)]
        """
        r = np.array([[np.cos(phi), -np.sin(phi)],[np.sin(phi), np.cos(phi)]])
        return r

    def horizontal_line_segment_intersection(self,a1,a2,b1,b2) -> float:
        """
        assuming that all these 4 points fall on one line, 
        the function returns the length of the intersection of line segments
        a1-a2 and b1-b2
        """
        # make sure they are sorted
        a1x = a1[0]
        a2x = a2[0]
        b1x = b1[0]
        b2x = b2[0]
        if a2[0] < a1[0]:
            a1x = a2[0]
            a2x = a1[0]
        if b2[0] < b1[0]:
            b1x = b2[0]
            b2x = b1[0]
        x1=max(a1x,b1x)
        x2=min(a2x,b2x)
        return [x1,x2]

    def cube_cube(self):        
        pass

    def is_infinitesimal(self) -> bool:
        if self.__does_intersect:
            return self.__is_infinitestimal
        else:
            raise Exception("don't call this function if you haven't checked does_intersect first :D")

    def get_intersection_point(self):
        return self._intersection_point