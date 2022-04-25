from cmath import pi
import numpy as np
import physical_object
from simulator.position import Position
import copy


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
                bump_point = in_in.get_intersection_point()
                
                center_point = np.array([self.position.x,\
                    self.position.y,self.position.z])
                
                center_to_bump_unit_vector = (bump_point - center_point)/\
                    np.linalg.norm(bump_point - center_point)
                orientation_unit_vector = np.array(self.polar_to_cartesian(1,\
                    self.position.phi,self.position.theta))
                # TODO replace the epsilon 
                if np.linalg.norm(orientation_unit_vector - center_to_bump_unit_vector) < 1e-5:
                    new_orientation_unit_vector = - center_to_bump_unit_vector
                else:
                    normal_vector = np.cross(orientation_unit_vector, \
                        center_to_bump_unit_vector)
                    mirror_unit_vector = np.cross(center_to_bump_unit_vector, normal_vector)
                    mirror_vector = np.dot(mirror_unit_vector, orientation_unit_vector) * \
                        mirror_unit_vector
                    delta_vector = mirror_vector - orientation_unit_vector
                    new_orientation_unit_vector = orientation_unit_vector + 2 * delta_vector

                # a check only to know the math works fine, otherwise being a unit
                # vector is not necessary
                if np.linalg.norm(new_orientation_unit_vector) != 1:
                    raise Exception("new orientation vector norm is " + \
                        str(np.linalg.norm(new_orientation_unit_vector)))
                
                # returning here, i.e. doing one intersection only as the point object
                # cannot bump into two objects :D
                tmp = self.cartesian_to_polar(*new_orientation_unit_vector)
                new_position = copy.copy(self.position)
                new_position.phi = tmp[1]
                new_position.theta = tmp[2]
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
        phi = np.arctan2(y,y) * 180/ np.pi

        # TODO do we need to keep the quanities in position in native data types?
        return [float(r), float(phi), float(theta)]
    
    def get_required_delta_t(self) -> float:
        """returns the delta_t that this object requires to operate right.
           returns 0 if the objects declares no requirement.
        """
        # TODO just some dummy value
        return 2* self.shape.radius / self.velocity / 100
        


                
