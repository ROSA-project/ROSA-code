import numpy as np
import physical_object
from position import Position
import copy
import logger

# TODO move
non_zero_criterion = 0.0001


class RigidPointBall(physical_object.RigidPhysicalObject):
    """
    A rigid ball that reflects from the bump surface. It is a point object as it does
    not rotate
    """

    def new_position_upon_bump(self) -> Position:
        """
            handles the new direction of movement when a bump has happened.
            That is, we're here because infinitesimal intersections had occurred in the
            previous cycle.
            TODO assuming other objects are still, meaning that we have no change in
                momentum in other words we are not currently modelling bump of two moving
                objects
            outputs:
                a position object carrying new orientation. i.e. the cartesian part is not
                 used
        """
        for in_in in self._latest_intersections:
            if in_in.does_intersect() and in_in.is_infinitesimal():
                # TODO I'm taking the first bump, process and return! we can have
                # multiple bumps at the same time resulting in a combined change.

                # TODO we won't have this method. just an oversimplification for now
                # bump_point expected to be a numpy array with 3 elements x, y and z
                logger.Logger.add_line("processing a bump:")

                intersection_points = in_in.get_intersection_point()
                # TODO temporary: average two intersection points to find the bump point.
                bump_point = 1 / 2 * (intersection_points[0][0] + intersection_points[0][1])
                logger.Logger.add_line("given bump point = " + str(bump_point))

                center_point = np.array([self.position.x, self.position.y,
                                         self.position.z])
                logger.Logger.add_line("circle (ball) center = " + str(center_point))

                new_phi, new_theta = RigidPointBall.calculate_circle_bounce(
                    center_point, self.position.phi, self.position.theta, bump_point)

                new_position = copy.copy(self.position)
                new_position.phi = new_phi
                new_position.theta = new_theta
                logger.Logger.add_line("phi and theta changed from " + str(
                    self.position.phi) + ", " + str(self.position.theta) + " to " +
                                       str(new_phi) + ", " + str(new_theta))
                logger.Logger.add_line("processing a bump finished.")
                return new_position

    def calculate_circle_bounce(circle_center, phi, theta, bump_point):
        """
        consider a circle that hits a surface. No matter the shape of the surface,
        the circle hits it at a point on its perimeter. circle's direction of movement
        and center and bump point is enough to calculate the direction of reflection (bounce)
        Note that circle radius plays no role, as the bump point defines the new effective
        radius.
        inputs:
            circle_center: a list of three numbers x y and z
            bump_point: the same
            phi, theta: degrees describing direction of circle's movement, according to
                to standard spherical coordinate system.
        outputs:
            new phi and theta
        """
        center_to_bump_unit_vector = (bump_point - circle_center) / \
                                     np.linalg.norm(bump_point - circle_center)
        logger.Logger.add_line("center_to_bump_unit_vector = " + str(
            center_to_bump_unit_vector))

        orientation_unit_vector = np.array(RigidPointBall.polar_to_cartesian(1, phi, theta))
        logger.Logger.add_line("orientation_unit_vector = " + str(
            orientation_unit_vector))

        if np.linalg.norm(orientation_unit_vector - center_to_bump_unit_vector) < \
                non_zero_criterion:
            # face-2-face bump
            new_orientation_unit_vector = - center_to_bump_unit_vector
            logger.Logger.add_line("orientation_unit_vector ~= "
                                   "center_to_bump_unit_vector so new_orientation_unit"
                                   "_vector = " + str(new_orientation_unit_vector))
        elif np.linalg.norm(orientation_unit_vector + center_to_bump_unit_vector) < \
                non_zero_criterion:
            # bump from back
            new_orientation_unit_vector = orientation_unit_vector
        else:
            normal_vector = np.cross(orientation_unit_vector, center_to_bump_unit_vector)
            logger.Logger.add_line("normal_vector = " + str(normal_vector))

            mirror_unit_vector = np.cross(center_to_bump_unit_vector, normal_vector)
            mirror_unit_vector = mirror_unit_vector / np.linalg.norm(mirror_unit_vector)
            logger.Logger.add_line("mirror_unit_vector = " + str(mirror_unit_vector))

            mirror_vector = np.dot(mirror_unit_vector, orientation_unit_vector) * \
                            mirror_unit_vector
            logger.Logger.add_line("mirror_vector = " + str(mirror_vector))

            delta_vector = mirror_vector - orientation_unit_vector
            logger.Logger.add_line("delta_vector = " + str(delta_vector))

            new_orientation_unit_vector = orientation_unit_vector + 2 * delta_vector
            logger.Logger.add_line("new_orientation_unit_vector = " + str(
                new_orientation_unit_vector))

        # a check only to know the math works fine, otherwise being a unit
        # vector is not necessary
        if abs(np.linalg.norm(new_orientation_unit_vector) - 1) > non_zero_criterion:
            raise Exception("new orientation vector norm is " + str(np.linalg.norm(
                new_orientation_unit_vector)))

        # returning here, i.e. doing one intersection only as the point object
        # cannot bump into two objects :D
        tmp = RigidPointBall.cartesian_to_polar(*new_orientation_unit_vector)
        new_phi = tmp[1]
        new_theta = tmp[2]
        return new_phi, new_theta

    def polar_to_cartesian(r, phi_degree, theta_degree):
        x = r * np.sin(theta_degree * np.pi / 180) * np.cos(phi_degree * np.pi / 180)
        y = r * np.sin(theta_degree * np.pi / 180) * np.sin(phi_degree * np.pi / 180)
        z = r * np.cos(theta_degree * np.pi / 180)
        return [x, y, z]

    def cartesian_to_polar(x, y, z):
        r = np.sqrt(x * x + y * y + z * z)
        # TODO these arc functions need correct handling
        theta = np.arccos(z / r) * 180 / np.pi  # to degrees
        phi = np.arctan2(y, x) * 180 / np.pi

        # TODO do we need to keep the qualities in position in native data types?
        return [float(r), float(phi), float(theta)]

    def get_required_delta_t(self) -> float:
        """returns the delta_t that this object requires to operate right.
           returns 0 if the objects declares no requirement.
        """
        # TODO just some dummy value
        return 2 * self.shape.radius / self.velocity / 200
