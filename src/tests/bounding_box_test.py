import unittest
import sys

sys.path.append(r"src/simulator")
import json
import testing_tools as teto
from cube import Cube
from cylinder import Cylinder
from position import Position

json_path_prefix = "src/tests/"


class BoundingBoxTest(unittest.TestCase):
    def test_bounding_box(self):
        json_filename = json_path_prefix + "bounding_box_test_input.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i=test_counter):
                if testcases[testcase]["type"] == "Cube":
                    c = Cube(testcases[testcase]["dimension"][0],
                             testcases[testcase]["dimension"][1],
                             testcases[testcase]["dimension"][2])
                elif testcases[testcase]["type"] == "Cylinder":
                    c = Cylinder(testcases[testcase]["dimension"][0], testcases[testcase]["dimension"][1])

                position = Position(testcases[testcase]["position"][0],
                                    testcases[testcase]["position"][1],
                                    testcases[testcase]["position"][2],
                                    testcases[testcase]["rotation_angle"][0],
                                    testcases[testcase]["rotation_angle"][1])
                bounding_box = c.bounding_box(position)
                dimension_box = [bounding_box.shape.length, bounding_box.shape.width, bounding_box.shape.height]
                self.assertTrue(teto.matrix_almost_equal(dimension_box,
                                                         testcases[testcase]["expected_dimension_box"])
                                , msg=testcase)


if __name__ == '__main__':
    unittest.main()

