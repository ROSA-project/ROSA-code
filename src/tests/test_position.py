import unittest
import json
import sys

sys.path.append("src/simulator")
import src.simulator.position as position

json_path_prefix = "src/tests/"


class MyTestCase(unittest.TestCase):
    def test_calculate_orientation_quaternion(self):
        # TODO: add more testcases
        json_filename = json_path_prefix + "orientation_quaternion.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i=test_counter):
                point = position.Position(testcases[testcase]["x"], testcases[testcase]["y"], testcases[testcase]["z"],
                                          testcases[testcase]["theta"], testcases[testcase]["phi"])
                q = point.calculate_orientation_quaternion(testcases[testcase]["h"])
                self.assertAlmostEqual(q.rotate(testcases[testcase]["point"])[0],
                                       testcases[testcase]["expected_output"][0], msg=testcase + " x")
                self.assertAlmostEqual(q.rotate(testcases[testcase]["point"])[1],
                                       testcases[testcase]["expected_output"][1], msg=testcase + " y")
                self.assertAlmostEqual(q.rotate(testcases[testcase]["point"])[2],
                                       testcases[testcase]["expected_output"][2], msg=testcase + " z")
            test_counter += 1


if __name__ == '__main__':
    unittest.main()
