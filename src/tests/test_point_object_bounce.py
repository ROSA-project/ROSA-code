import unittest

import sys
sys.path.append("simulator")
#sys.path.append(r"visualizer")

import ball
import numpy as np

radians_accuracy_decimal_points = 10
class PointObjectBounce(unittest.TestCase):
    def test_circle_bounce(self):
        circle_center = [0, 0, 0]
        phi = 0
        theta = 90
        bump_point = [1, 0, 0]
        
        expected_phi = -np.pi
        expected_theta = 0

        new_phi, new_theta = ball.RigidPointBall.calculate_circle_bounce(\
                            circle_center,phi,theta,bump_point)
        
        self.assertEqual(round(new_phi - expected_phi, radians_accuracy_decimal_points),0)
        self.assertEqual(round(new_theta - expected_theta, radians_accuracy_decimal_points),0)

if __name__ == '__main__':
    unittest.main()