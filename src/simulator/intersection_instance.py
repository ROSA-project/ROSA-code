from __future__ import annotations
import logger
import object
import numpy as np

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
        self.__does_intersect = False
        self.__is_infinitesimal = False
        self._intersection_points = []
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
            self.cylinder_cube()
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

    def cylinder_cube(self):
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
                                                                               "radius "
                                                                               "= " +
                               str(circle_radius))

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
                      [circle_center[0] - circle_radius, circle_center[1]],
                      [circle_center[0] + circle_radius, circle_center[1]])) == 0:
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

    def is_infinitesimal(self) -> bool:
        if self.__does_intersect:
            return self.__is_infinitesimal
        else:
            raise Exception(
                "don't call this function if you haven't checked does_intersect first :D")

    def get_intersection_point(self):
        if not self._intersection_points:
            raise Exception(
                "no intersection recorded., the method must not have been called")
        return self._intersection_points
