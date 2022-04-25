import numpy as np
import physical_object
from simulator.position import Position
import copy
import logger


# TODO move
non_zero_criterion = 0.0001

class RigidPointBall(physical_object.RigidPhysicalObject):
    """
    easier to model as dump points are easy to calculate for a sphere
    following the light reflection model, ignoring mass and acceleration. 
    decrease the ball radius if you want it to look real.
    """
    def new_position_upon_bump(self) -> Position:
        #recall that we're here because infinitesimal intersections had occured in the
        #previous cycle. 
        for in_in in self._latest_intersections:
            if in_in.does_intersect() and in_in.is_infinitesimal():
                # TODO I'm taking the first bump, process and return! we can have
                # multiple bumps at the same time resulting in a combined change.
                
                # TODO we won't have this method. just an oversimplification for now
                #bump_point expected to be a numpy array with 3 elements x, y and z
                logger.Logger.add_line("processing a bump:")
                
                bump_point = in_in.get_intersection_point()
                logger.Logger.add_line("given bump point = " + str(bump_point))
                
                center_point = np.array([self.position.x,\
                    self.position.y,self.position.z])
                logger.Logger.add_line("circle (ball) center = " + str(center_point))
                
                center_to_bump_unit_vector = (bump_point - center_point)/\
                    np.linalg.norm(bump_point - center_point)
                logger.Logger.add_line("center_to_bump_unit_vector = " + \
                    str(center_to_bump_unit_vector))
                
                orientation_unit_vector = np.array(self.polar_to_cartesian(1,\
                    self.position.phi,self.position.theta))
                logger.Logger.add_line("orientation_unit_vector = " + \
                    str(orientation_unit_vector))
                
                # TODO replace the epsilon 
                if np.linalg.norm(orientation_unit_vector - center_to_bump_unit_vector) < non_zero_criterion:
                    new_orientation_unit_vector = - center_to_bump_unit_vector
                    logger.Logger.add_line("orientation_unit_vector ~= center_to_bump_unit_vector so " + \
                        "new_orientation_unit_vector = " + str(new_orientation_unit_vector))
                else:
                    normal_vector = np.cross(orientation_unit_vector, \
                        center_to_bump_unit_vector)
                    logger.Logger.add_line("normal_vector = " + \
                        str(normal_vector))    
                
                    mirror_unit_vector = np.cross(center_to_bump_unit_vector, normal_vector)
                    mirror_unit_vector = mirror_unit_vector / np.linalg.norm(mirror_unit_vector)
                    logger.Logger.add_line("mirror_unit_vector = " + \
                        str(mirror_unit_vector))
                
                    mirror_vector = np.dot(mirror_unit_vector, orientation_unit_vector) * \
                        mirror_unit_vector
                    logger.Logger.add_line("mirror_vector = " + \
                        str(mirror_vector))
                
                    delta_vector = mirror_vector - orientation_unit_vector
                    logger.Logger.add_line("delta_vector = " + \
                        str(delta_vector))
                
                    new_orientation_unit_vector = orientation_unit_vector + 2 * delta_vector
                    logger.Logger.add_line("new_orientation_unit_vector = " + \
                        str(new_orientation_unit_vector))

                # a check only to know the math works fine, otherwise being a unit
                # vector is not necessary
                if abs(np.linalg.norm(new_orientation_unit_vector)- 1) > non_zero_criterion:
                    raise Exception("new orientation vector norm is " + \
                        str(np.linalg.norm(new_orientation_unit_vector)))
                
                # returning here, i.e. doing one intersection only as the point object
                # cannot bump into two objects :D
                tmp = self.cartesian_to_polar(*new_orientation_unit_vector)
                new_position = copy.copy(self.position)
                new_position.phi = tmp[1]
                new_position.theta = tmp[2]
                logger.Logger.add_line("phi and theta changed from " + str(self.position.phi) \
                    + ", " + str(self.position.theta) + " to " + str(tmp[1]) + ", " + str(tmp[2]))
                logger.Logger.add_line("processing a bump finished.")    
                return new_position
                
    def polar_to_cartesian(self,r,phi_degree,theta_degree):
        x= r * np.sin(theta_degree * np.pi/180) * \
            np.cos(phi_degree * np.pi/180)
        y= r * np.sin(theta_degree * np.pi/180) * \
            np.sin(phi_degree * np.pi/180)
        z= r * np.cos(theta_degree * np.pi/180)
        return [x,y,z]

    def cartesian_to_polar(self,x,y,z):
        r = np.sqrt(x*x + y*y + z*z)
        # TODO these arc functions need correct handling
        theta = np.arccos(z/r) * 180/ np.pi #to degrees
        phi = np.arctan2(y,x) * 180/ np.pi

        # TODO do we need to keep the quanities in position in native data types?
        return [float(r), float(phi), float(theta)]
    
    def get_required_delta_t(self) -> float:
        """returns the delta_t that this object requires to operate right.
           returns 0 if the objects declares no requirement.
        """
        # TODO just some dummy value
        return 2* self.shape.radius / self.velocity / 200
        


                
