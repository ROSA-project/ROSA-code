import unittest
import sys
sys.path.append(r"src/simulator")
import json
import testing_tools as teto
from shape import Shape

json_path_prefix = "src/tests/"


class RotationPoints(unittest.TestCase):
    def test_rotation_point(self):
        json_filename = json_path_prefix + "rotation_points.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)

            test_counter = 0
            for testcase in testcases:
                with self.subTest(i=test_counter):
                    rotation_points = Shape.rotation(testcases[testcase]["position"][0],
                                                     testcases[testcase]["position"][1],
                                                     testcases[testcase]["position"][2],
                                                     testcases[testcase]["phi"],
                                                     testcases[testcase]["theta"])
                    self.assertTrue(teto.matrix_almost_equal(rotation_points,
                                                             testcases[testcase]["expected_point"])
                                    , msg=testcase)


if __name__ == '__main__':
    unittest.main()