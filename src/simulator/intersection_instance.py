from __future__ import annotations

import math

import saeed_logger as logger
import object
import box
import cube
import position
import numpy as np
import copy
import pyquaternion as pq

# TODO move
epsilon_criterion = 0.1
non_zero_criterion = 0.0001


class IntersectionInstance:
    """performs intersection between two objects and stores the result. 
       # TODO currently a sketch. Interface no defined right.
    """

    def __init__(self, object1: object.Object, object2: object.Object):
        self.object1 = object1
        self.object2 = object2
        self.acceptable_volume_of_intersection = 10
        self.accuracy = 1
        self.__does_intersect = False
        self.__is_infinitesimal = False
        self._intersection_points = []
        self._intersection_point = []
        self.intersect()

    def intersect(self) -> dict:
        """
            the entry point for performing the intersection algorithm on its two
            objects
            No return value, the other methods do the job.
            The results are then taken by calling methods such as does_intersect,
            is_infinitesimal and so on.
        """
        # TODO a temporary implementation for pairs of supported geometrical shapes
        shape_classes = [(self.object1.shape.dump_info())["type"],
                         (self.object2.shape.dump_info())["type"]]

        if "Cylinder" in shape_classes and "Cube" in shape_classes:
            self.cylinder_cube_intersection()
        elif shape_classes == ["Cube", "Cube"]:
            self.cube_cube()
        elif shape_classes == ["Cylinder", "Cylinder"]:
            self.cylinder_cylinder()
        else:
            raise Exception("Cannot intersect the given objectIDs " + str(
                self.object1.oid) + " and " + str(self.object2.oid) + " with shapes " +
                            shape_classes[0] + ", " + shape_classes[1])

    def does_intersect(self) -> bool:
        """
        merely provides access to internal attribute
        """
        return self.__does_intersect

    def cylinder_cube(self) -> None:
        """
        performs intersection and populates:
            self._intersection_points
            self.__is_infinitesimal
        # TODO temporary interface, to be completed once complete intersection is 
            implemented
        """
        # TODO assuming objects with theta=0, i.e upright and intersecting 2D

        if (self.object1.shape.dump_info())["type"] == "Cylinder":
            cylinder_object = self.object1
            cube_object = self.object2
        else:
            cylinder_object = self.object2
            cube_object = self.object1

        circle_radius = cylinder_object.shape.radius
        circle_center = [cylinder_object.position.x, cylinder_object.position.y]

        # TODO in our code length and width are not well defined but visualization is
        #  taking width as y-axis-side and so on. important for the input to the
        #  following function
        rectangle_length = cube_object.shape.length
        rectangle_width = cube_object.shape.width
        rectangle_center = [cube_object.position.x, cube_object.position.y]
        rectangle_phi_rad = cube_object.position.phi * np.pi / 180

        # find the 4 lines of the cube(recatngle) and run line-circle intersections
        lines = IntersectionInstance.rectangle_lines(rectangle_center,
                                                     rectangle_length, rectangle_width,
                                                     rectangle_phi_rad)

        intersection_points_distance = []
        intersection_points = []
        for line in lines:
            new_intersection_points, new_intersection_distance = \
                IntersectionInstance.line_circle(line[0], line[1], circle_center,
                                                 circle_radius)

            logger.Logger.add_line("oid's " + str(self.object1.oid) + " , " + str(
                self.object2.oid) + ": intersection points distance = " + str(
                new_intersection_distance))

            # if no intersection this will be -1
            intersection_points_distance.append(new_intersection_distance)

            if len(new_intersection_points) > 0:
                intersection_points.append(new_intersection_points)

        self._intersection_points = intersection_points

        # TODO strictly larger than 0 must be documented. see calculation of the distance
        if max(intersection_points_distance) > non_zero_criterion:
            self.__does_intersect = True
            if max(intersection_points_distance) > epsilon_criterion:
                self.__is_infinitesimal = False
            else:
                self.__is_infinitesimal = True

    def line_circle(p1, p2, circle_center, circle_radius):
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
            the return value is a tupe of 
                -the points showing the intersection of the
            two line segments p1-p2 and i1-i2.
                -the distance of the points.
        """
        # indicating no intersection
        intersection_points = []

        if p1[0] == p2[0]:
            phi_rad = np.pi / 2
        else:
            # m = (p2[1] - p1[1]) / (p2[0]-p1[0]) #slope
            # TODO arc
            phi_rad = np.arctan2((p2[1] - p1[1]), (p2[0] - p1[0]))

        r_matrix = IntersectionInstance.rotation_matrix_2d(-phi_rad)

        logger.Logger.add_line("line-circle intersection:")
        logger.Logger.add_line("input line = " + str(p1) + " , " + str(p2))
        logger.Logger.add_line("input circle center = " + str(circle_center) + " and "
                                                                               "radius = " + str(circle_radius))

        p1 = r_matrix.dot(p1)
        p2 = r_matrix.dot(p2)
        circle_center = r_matrix.dot(circle_center)

        logger.Logger.add_line("rotated line =" + str(p1) + " , " + str(p2))
        logger.Logger.add_line("rotated circle center " + str(circle_center))

        if p1[1] < circle_center[1] - circle_radius or \
                p1[1] > circle_center[1] + circle_radius:
            # vertically separated
            # logger.Logger.add_line("vertically separated")
            intersect_points_distance = -1
        elif np.linalg.norm(
                IntersectionInstance.horizontal_line_segment_intersection(p1, p2,
                                                                          [circle_center[0] - circle_radius,
                                                                           circle_center[1]],
                                                                          [circle_center[0] + circle_radius,
                                                                           circle_center[1]])) == 0:
            # horizontally separated
            # logger.Logger.add_line("horizontally separated")
            intersect_points_distance = -1
        else:
            # logger.Logger.add_line("need to calculate the intersection")
            m = 0
            h = p1[1] - m * p1[0]
            a = 1 + m ** 2
            b = 2 * m * h - 2 * m * circle_center[1] - 2 * circle_center[0]
            c = circle_center[0] ** 2 + h ** 2 + circle_center[1] ** 2 - 2 * h * \
                circle_center[1] \
                - circle_radius ** 2
            delta = b ** 2 - 4 * a * c
            if delta < 0:
                # no solution
                intersect_points_distance = -1
                logger.Logger.add_line("delta < 0")
            else:
                # two distinct or equal solutions
                # x1 < x2
                x1 = (-b - np.sqrt(delta)) / (2 * a)
                x2 = (-b + np.sqrt(delta)) / (2 * a)
                y1 = m * x1 + h
                y2 = m * x2 + h
                x_intersect_points = \
                    IntersectionInstance.horizontal_line_segment_intersection([x1, y1],
                                                                              [x2, y2],
                                                                              p1, p2)
                if x_intersect_points == 0:
                    # meaning no intersection
                    intersection_points = []
                    intersect_points_distance = -1
                    return [], -1

                # undo the rotation
                # TODO hardcoding a zero for z
                r_inv_matrix = IntersectionInstance.rotation_matrix_2d(phi_rad)
                tmp0 = r_inv_matrix.dot([x_intersect_points[0], p1[1]])
                tmp1 = r_inv_matrix.dot([x_intersect_points[1], p1[1]])
                intersection_points = np.array([[tmp0[0], tmp0[1], 0],
                                                [tmp1[0], tmp1[1], 0]])

                intersect_points_distance = abs(
                    x_intersect_points[0] - x_intersect_points[1])

        return intersection_points, intersect_points_distance

    def rectangle_lines(center: list[float], x_axis_side: float, y_axis_side: float,
                        phi_rad: float):
        """
            return values is a numpy array, a matrix of vectors each being a line
        """
        # TODO assuming that cube position is at its center
        points = [[-x_axis_side / 2, -y_axis_side / 2],
                  [+x_axis_side / 2, -y_axis_side / 2],
                  [+x_axis_side / 2, +y_axis_side / 2],
                  [-x_axis_side / 2, +y_axis_side / 2]]
        # now rotate by phi
        r_matrix = IntersectionInstance.rotation_matrix_2d(phi_rad)
        points = r_matrix.dot((np.array(points)).T).T
        points = points + np.array(center)
        lines = [[points[0], points[1]],
                 [points[1], points[2]],
                 [points[2], points[3]],
                 [points[3], points[0]]]
        logger.Logger.add_line(
            "For the rectangle with center at " + str(center) + ", x_side = " + str(
                x_axis_side) + ", y_axis = " + str(y_axis_side) + ", the points are:")
        logger.Logger.add_line(str(lines))
        return lines

    def rotation_matrix_2d(phi: float):
        """
        phi in radians
        [ cos(phi)  -sin(phi)
          sin(phi)   cos(phi)]
        """
        r = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
        return r

    def horizontal_line_segment_intersection(a1, a2, b1, b2) -> list:
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

        x1 = max(a1x, b1x)
        x2 = min(a2x, b2x)
        if x1 > x2:
            # means they do not intersect
            return 0
        else:
            return [x1, x2]

    def cube_cube(self):
        # TODO to be implemented        
        pass

    def cylinder_cylinder(self):
        # TODO to be implemented        
        pass

    @staticmethod
    def average_point(points: list) -> list:
        """
        Gets a list of points and returns the average point of it in the form of [average_x,average_y,average_z]
        """
        if len(points) == 0:
            raise ValueError("The given list has no points")
        sum_of_x = 0
        sum_of_y = 0
        sum_of_z = 0
        number_of_points = len(points)
        for point in points:
            sum_of_x += point[0]
            sum_of_y += point[1]
            sum_of_z += point[2]
        return [sum_of_x / number_of_points, sum_of_y / number_of_points, sum_of_z / number_of_points]

    @staticmethod
    def is_in_cylinder(cylinder_obj: object.Object, point: list) -> bool:
        """
        Checks whether the given point is in the given axis-aligned cylinder or not.
        Args:
            cylinder: an axis-aligned cylinder
            point: a list of coordinates of the point in the form of [x,y,z]
        """
        if (point[0] - cylinder_obj.position.x) ** 2 + (point[1] - cylinder_obj.position.y) ** 2 < (
                cylinder_obj.shape.radius) ** 2 or np.isclose(
            (point[0] - cylinder_obj.position.x) ** 2 + (point[1] - cylinder_obj.position.y) ** 2, (
                                                                                                           cylinder_obj.shape.radius) ** 2):
            if ((point[2] < cylinder_obj.position.z + (cylinder_obj.shape.height / 2)) or np.isclose(point[2],
                                                                                                     cylinder_obj.position.z + (
                                                                                                             cylinder_obj.shape.height / 2))) and (
                    point[2] > cylinder_obj.position.z - (cylinder_obj.shape.height / 2) or np.isclose(point[2],
                                                                                                       cylinder_obj.position.z - (
                                                                                                               cylinder_obj.shape.height / 2))):
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def is_in_cube(cube_obj: object.Object, point: list) -> bool:
        """
        Checks whether the given point is in the given axis-aligned cube or not.
        Args:
            cube: an axis-aligned cube
            point: a list of coordinates of the point in the form of [x,y,z]
        """
        if ((cube_obj.position.x - (cube_obj.shape.length / 2)) < point[0] or np.isclose(point[0], (
                cube_obj.position.x - (cube_obj.shape.length / 2)))) and (
                (cube_obj.position.x + (cube_obj.shape.length / 2)) > \
                point[0] or np.isclose(point[0], cube_obj.position.x + (cube_obj.shape.length / 2))):
            if ((cube_obj.position.y - (cube_obj.shape.width / 2)) < point[1] or np.isclose(point[1],
                                                                                            cube_obj.position.y - (
                                                                                                    cube_obj.shape.width / 2))) and (
                    (
                            cube_obj.position.y + (cube_obj.shape.width / 2)) > \
                    point[1] or np.isclose(point[1], cube_obj.position.y + (cube_obj.shape.width / 2))):
                if ((cube_obj.position.z - (cube_obj.shape.height / 2)) < point[2] or np.isclose(point[2],
                                                                                                 cube_obj.position.z - (
                                                                                                         cube_obj.shape.height / 2))) and (
                        (
                                cube_obj.position.z + (cube_obj.shape.height / 2)) > point[2] or np.isclose(point[2],
                                                                                                            cube_obj.position.z + (
                                                                                                                    cube_obj.shape.height / 2))):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    @staticmethod
    def intersection_of_intervals(first_interval: list[float], second_interval: list[float]) -> list[float]:
        """
        Gets two closed intervals and returns the intersection of them, if there's no intersection then it returns None
        """
        if (first_interval[1] <= second_interval[0]) or (first_interval[0] >= second_interval[1]):
            return None
        else:
            start = max(first_interval[0], second_interval[0])
            end = min(first_interval[1], second_interval[1])
            if np.isclose(end - start, 0):
                return None
            return [start, end]

    @staticmethod
    def intersection_of_bounding_boxes(box1: box.Box, box2: box.Box) -> box.Box:
        """
        Gets two bounding boxes and returns the box of their intersection, if there's no intersection it returns None
        """
        interval_of_x1 = [box1.position.x - (box1.shape.length / 2), box1.position.x + (box1.shape.length / 2)]
        interval_of_x2 = [box2.position.x - (box2.shape.length / 2), box2.position.x + (box2.shape.length / 2)]
        interval_of_y1 = [box1.position.y - (box1.shape.width / 2), box1.position.y + (box1.shape.width / 2)]
        interval_of_y2 = [box2.position.y - (box2.shape.width / 2), box2.position.y + (box2.shape.width / 2)]
        interval_of_z1 = [box1.position.z - (box1.shape.height / 2), box1.position.z + (box1.shape.height / 2)]
        interval_of_z2 = [box2.position.z - (box2.shape.height / 2), box2.position.z + (box2.shape.height / 2)]
        interval_of_x = IntersectionInstance.intersection_of_intervals(interval_of_x1, interval_of_x2)
        interval_of_y = IntersectionInstance.intersection_of_intervals(interval_of_y1, interval_of_y2)
        interval_of_z = IntersectionInstance.intersection_of_intervals(interval_of_z1, interval_of_z2)
        if interval_of_x is None or interval_of_y is None or interval_of_z is None:
            return None
        else:
            length = interval_of_x[1] - interval_of_x[0]
            width = interval_of_y[1] - interval_of_y[0]
            height = interval_of_z[1] - interval_of_z[0]
            # TODO: Should I pass objectRegistry to intersection_box?
            intersection_box = box.Box(oid=None, name="intersection box",
                                       cube=cube.Cube(length=length, height=height, width=width),
                                       position=position.Position((interval_of_x[1] + interval_of_x[0]) / 2,
                                                                  (interval_of_y[1] + interval_of_y[0]) / 2,
                                                                  (interval_of_z[1] + interval_of_z[0]) / 2, 0, 0),
                                       owner_object=None, registry=None)
            return intersection_box

    @staticmethod
    def parametric_line_equation(first_point: list[float], second_point: list[float]) -> list[float]:
        """
        Gets two points and returns the parametric line equation in the form of [point, direction_vector]
        """
        direction_vector = [second_point[0] - first_point[0], second_point[1] - first_point[1],
                            second_point[2] - first_point[2]]
        if direction_vector == [0, 0, 0]:
            raise ValueError("The given points are the same.")
        return [first_point, direction_vector]

    @staticmethod
    def convert_to_axis_aligned(obj: object.Object) -> object.Object:
        if obj.position.phi == 0 and obj.position.theta == 0:
            return obj
        else:
            orientation_quaternion = obj.position.calculate_orientation_quaternion(obj.shape.height)
            rotation_quaternion = orientation_quaternion.inverse
            center = [obj.position.x, obj.position.y, obj.position.z]
            rotated_center = rotation_quaternion.rotate(center)
            # TODO: Is it necessary to use deepcopy? if not, it's better not to use it because it's very slow
            axis_aligned_object = copy.deepcopy(obj)
            axis_aligned_object.position.x = rotated_center[0]
            axis_aligned_object.position.y = rotated_center[1]
            axis_aligned_object.position.z = rotated_center[2]
            axis_aligned_object.position.phi = 0
            axis_aligned_object.position.theta = 0
            return axis_aligned_object

    def cylinder_cube_intersection(self):
        if (self.object1.shape.dump_info())["type"] == "Cylinder":
            cylinder_object = self.object1
            cube_object = self.object2
        else:
            cylinder_object = self.object2
            cube_object = self.object1
        # Calculating bounding boxes of each object and their box of intersection
        bounding_box_of_cylinder = cylinder_object.shape.bounding_box(cylinder_object.position)
        bounding_box_of_cube = cube_object.shape.bounding_box(cube_object.position)
        # a copy of each of object which is axis-aligned
        intersection_box = IntersectionInstance.intersection_of_bounding_boxes(bounding_box_of_cylinder,
                                                                               bounding_box_of_cube)
        axis_aligned_cube = IntersectionInstance.convert_to_axis_aligned(cube_object)
        axis_aligned_cylinder = IntersectionInstance.convert_to_axis_aligned(cylinder_object)
        # calculating rotation quaternion for each object, so that one can apply the rotation that makes objects
        # axis-aligned to any point
        cube_rotation_quaternion = cube_object.position.calculate_orientation_quaternion(
            cube_object.shape.height).inverse
        cylinder_rotation_quaternion = cylinder_object.position.calculate_orientation_quaternion(
            cylinder_object.shape.height).inverse
        # If there's no intersection between the bounding boxes we are done.
        if intersection_box == None:
            self.__does_intersect = False
            return
        else:
            # number of internal points in each direction:
            l = math.floor((intersection_box.shape.length / self.accuracy) + 1)
            w = math.floor((intersection_box.shape.width / self.accuracy) + 1)
            h = math.floor((intersection_box.shape.height / self.accuracy) + 1)
            # we choose the point with the smallest coordinates in the intersection box as the first internal point
            # to check
            starting_point = [intersection_box.position.x - (intersection_box.shape.length / 2),
                              intersection_box.position.y - (intersection_box.shape.width / 2),
                              intersection_box.position.z - (intersection_box.shape.height / 2)]
            # keeping track of the maximum coordinates, so that later we can compute the volume of intersection
            max_x = max_y = max_z = -1 * math.inf
            min_x = min_y = min_z = math.inf
            # generating internal points with the given accuracy and checking each internal point to see whether it's
            # in the intersection of the two objects or not
            for i in range(l):
                for j in range(w):
                    for k in range(h):
                        point = [starting_point[0] + (i * self.accuracy), starting_point[1] + (j * self.accuracy),
                                 starting_point[2] + (k * self.accuracy)]
                        # checks to make sure the generated point is in the intersection box:
                        if IntersectionInstance.is_in_cube(intersection_box, point):
                            if IntersectionInstance.is_in_cube(axis_aligned_cube, cube_rotation_quaternion.rotate(
                                    point)) and IntersectionInstance.is_in_cylinder(axis_aligned_cylinder,
                                                                                    cylinder_rotation_quaternion.rotate(
                                                                                        point)):
                                self._intersection_points.append(point)
                                # adjusting the maximum of coordinates according to the new intersection point
                                if point[0] > max_x:
                                    max_x = point[0]
                                elif point[0] < min_x:
                                    min_x = point[0]
                                if point[1] > max_y:
                                    max_y = point[1]
                                elif point[1] < min_y:
                                    min_y = point[1]
                                if point[2] > max_z:
                                    max_z = point[2]
                                elif point[2] < min_z:
                                    min_z = point[2]
                        else:
                            break
            # calculating the volume of the smallest cube containing all the intersecting points
            volume_of_intersection = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
            if len(self._intersection_points) != 0:
                self.__does_intersect = True
                self._intersection_point = IntersectionInstance.average_point(self._intersection_points)
                if volume_of_intersection <= self.acceptable_volume_of_intersection:
                    self.__is_infinitesimal = True
                else:
                    self.__is_infinitesimal = False
            else:
                self.__does_intersect = False

    def is_infinitesimal(self) -> bool:
        if self.__does_intersect:
            return self.__is_infinitesimal
        else:
            raise Exception(
                "don't call this function if you haven't checked does_intersect first :D")

    def get_intersection_points(self):
        if not self._intersection_points:
            raise Exception(
                "no intersection recorded., the method must not have been called")
        return self._intersection_points

    def get_intersection_point(self) -> list:
        return self._intersection_point
