import unittest

import sys
sys.path.append("simulator")
#sys.path.append(r"visualizer")

import ball
import numpy as np

radians_accuracy_decimal_points = 10
class PointObjectBounce(unittest.TestCase):
    def test_circle_bounce(self):
        circle_center = np.array([0, 0, 0])
        phi = 0
        theta = 90
        bump_point = np.array([1, 0, 0])
        
        expected_phi = -180
        expected_theta = 90

        new_phi, new_theta = ball.RigidPointBall.calculate_circle_bounce(\
                            circle_center,phi,theta,bump_point)
        
        self.assertTrue(self.angle_almost_equal(new_phi , expected_phi))
        self.assertTrue(self.angle_almost_equal(new_theta , expected_theta))

    def angle_almost_equal(self, angle1: float, angle2: float):
        modulo_value = 360
        return round(angle1 % modulo_value - angle2 % modulo_value, \
            radians_accuracy_decimal_points) == 0

if __name__ == '__main__':
    unittest.main()