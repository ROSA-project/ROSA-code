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

    def test_horizontal_line_segment_intersection(self):
        json_filename = "tests/horizontal_line_segment_intersection.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i = test_counter):
                lines = in_in.IntersectionInstance.horizontal_line_segment_intersection(\
                    testcases[testcase]["a1"], \
                    testcases[testcase]["a2"], \
                    testcases[testcase]["b1"], \
                    testcases[testcase]["b2"])
        
                self.assertTrue(teto.matrix_almost_equal(lines , 
                            testcases[testcase]["expected_interval"]), msg = testcase)                
            test_counter += 1

    def test_line_circle_intersection(self):
        json_filename = "tests/circle_line_intersection.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i = test_counter):
                new_intersection_points, new_intersection_distance = \
                    in_in.IntersectionInstance.line_circle(\
                    testcases[testcase]["p1"], \
                    testcases[testcase]["p2"], \
                    testcases[testcase]["circle_center"], \
                    testcases[testcase]["circle_radius"])
        
                self.assertTrue(teto.matrix_almost_equal(new_intersection_points , 
                    testcases[testcase]["expected_intersection_points"]),\
                    msg = testcase) 
                self.assertTrue(teto.matrix_almost_equal(new_intersection_distance , 
                    testcases[testcase]["expected_intersection_points_distance"]),\
                    msg = testcase)                
            test_counter += 1

if __name__ == '__main__':
    unittest.main()