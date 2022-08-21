import unittest
import json
import sys

sys.path.append("src/simulator")
json_path_prefix = "src/tests/"
import src.simulator.coordinate_conversion as conversion

class TestCylinderCubeIntersection(unittest.TestCase):

    def test_cylindrical_to_cartesian_coordinate(self):
        json_filename = json_path_prefix + "cylindrical_to_cartesian_coordinate.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i=test_counter):
                cartesian_coordinate = conversion.CoordinateConversion.cylindrical_to_cartesian_coordinate(
                    testcases[testcase]["r"],
                    testcases[testcase]["theta"],
                    testcases[testcase]["z"])
                expected_coordinate = testcases[testcase]["expected_output"]
                self.assertAlmostEqual(cartesian_coordinate["x"], expected_coordinate["x"], msg=testcase)
                self.assertAlmostEqual(cartesian_coordinate["y"], expected_coordinate["y"], msg=testcase)
                self.assertAlmostEqual(cartesian_coordinate["z"], expected_coordinate["z"], msg=testcase)
            test_counter += 1

    def test_spherical_to_cartesian_coordinate(self):
        json_filename = json_path_prefix + "spherical_to_cartesian_coordinate.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i=test_counter):
                cartesian_coordinate = conversion.CoordinateConversion.spherical_to_cartesian_coordinate(
                    testcases[testcase]["r"],
                    testcases[testcase]["theta"],
                    testcases[testcase]["phi"])
                expected_coordinate = testcases[testcase]["expected_output"]
                self.assertAlmostEqual(cartesian_coordinate["x"], expected_coordinate["x"], msg=testcase)
                self.assertAlmostEqual(cartesian_coordinate["y"], expected_coordinate["y"], msg=testcase)
                self.assertAlmostEqual(cartesian_coordinate["z"], expected_coordinate["z"], msg=testcase)
            test_counter += 1


if __name__ == '__main__':
    unittest.main()
