import unittest
import numpy as np
import sys
import json
sys.path.append("simulator")
#sys.path.append(r"visualizer")

import tests.testing_tools as teto
import ball

class PointObjectBounce(unittest.TestCase):
    def test_circle_bounce_from_still_rigid_object(self):
        json_filename = "tests/circle_bounce_from_still_rigid_object.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i = test_counter):
                new_phi, new_theta = ball.RigidPointBall.calculate_circle_bounce(\
                    np.array(testcases[testcase]["circle_center"]), \
                    testcases[testcase]["phi"], \
                    testcases[testcase]["theta"], \
                    np.array(testcases[testcase]["bump_point"]))
        
                self.assertTrue(teto.angle_almost_equal(new_phi , 
                            testcases[testcase]["expected_phi"]), msg = testcase)
                self.assertTrue(teto.angle_almost_equal(new_theta , 
                            testcases[testcase]["expected_theta"]),msg = testcase)
            test_counter += 1

if __name__ == '__main__':
    unittest.main()