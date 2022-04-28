import unittest
import numpy as np
import sys
import json
sys.path.append("simulator")

import tests.testing_tools as teto
import intersection_instance as in_in


class RectangleCircleIntersection(unittest.TestCase):
    def test_rectangle_to_lines_decomposition(self):
        json_filename = "tests/rectangle_to_lines_decomposition.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i = test_counter):
                lines = in_in.IntersectionInstance.rectangle_lines(\
                    testcases[testcase]["rectangle_center"], \
                    testcases[testcase]["x_axis_side"], \
                    testcases[testcase]["y_axis_side"], \
                    testcases[testcase]["phi_degree"] * np.pi/180)
        
                self.assertTrue(teto.matrix_almost_equal(lines , 
                            testcases[testcase]["expected_lines"]), msg = testcase)                
            test_counter += 1

if __name__ == '__main__':
    unittest.main()