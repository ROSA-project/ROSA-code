import math
import unittest
import json
import sys

sys.path.append("src/simulator")
json_path_prefix = "src/tests/"
import src.simulator.object as object
import src.simulator.cylinder as cylinder
import src.simulator.position as position
import src.simulator.cube as cube
import src.simulator.box as box
import src.tests.testing_tools as teto
import src.simulator.intersection_instance as in_in


class TestCylinderCubeIntersection(unittest.TestCase):
    def test_intersection_of_intervals(self):
        json_filename = json_path_prefix + "intersection_of_intervals.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            if testcases[testcase]["expected_output"] == "None":
                self.assertIsNone(
                    in_in.IntersectionInstance.intersection_of_intervals(testcases[testcase]["first_interval"],
                                                                         testcases[testcase]["second_interval"]),
                    msg=testcase)
            else:
                with self.subTest(i=test_counter):
                    self.assertListEqual(
                        in_in.IntersectionInstance.intersection_of_intervals(testcases[testcase]["first_interval"],
                                                                             testcases[testcase]["second_interval"]),
                        testcases[testcase]["expected_output"], msg=testcase)
                test_counter += 1

    def test_parametric_line_equation(self):
        self.assertListEqual(in_in.IntersectionInstance.parametric_line_equation([10, 15, 20], [-1, 6, 8]),
                             [[10, 15, 20], [-11, -9, -12]])
        with self.assertRaises(ValueError):
            in_in.IntersectionInstance.parametric_line_equation([1, 2, 3], [1, 2, 3])

    def test_average_point(self):
        self.assertListEqual(
            in_in.IntersectionInstance.average_point([[1, 2, 3], [-1, 12, 6], [1.2, -3.6, 7.8], [0, 0, 0]]),
            [0.3, 2.6, 4.2])
        self.assertListEqual(in_in.IntersectionInstance.average_point([[1.1, 2.2, 3.3]]), [1.1, 2.2, 3.3])
        with self.assertRaises(ValueError):
            in_in.IntersectionInstance.average_point([])

    def test_is_in_cylinder(self):
        json_filename = json_path_prefix + "is_in_cylinder.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            input_cylinder = object.Object(1, "Cylinder", cylinder.Cylinder(testcases[testcase]["radius"],
                                                                            testcases[testcase]["height"]),
                                           position.Position(testcases[testcase]["x"], testcases[testcase]["y"],
                                                             testcases[testcase]["z"], 0,
                                                             0), None, None)

            with self.subTest(i=test_counter):
                self.assertEqual(
                    in_in.IntersectionInstance.is_in_cylinder(input_cylinder, testcases[testcase]["point"]),
                    bool(testcases[testcase]["expected_output"]), msg=testcase)
            test_counter += 1

    def test_is_in_cube(self):
        json_filename = json_path_prefix + "is_in_cube.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            input_cube = object.Object(1, "Cube",
                                       cube.Cube(testcases[testcase]["length"], testcases[testcase]["height"],
                                                 testcases[testcase]["width"]),
                                       position.Position(testcases[testcase]["x"], testcases[testcase]["y"],
                                                         testcases[testcase]["z"], 0,
                                                         0), None, None)

            with self.subTest(i=test_counter):
                self.assertEqual(
                    in_in.IntersectionInstance.is_in_cube(input_cube, testcases[testcase]["point"]),
                    bool(testcases[testcase]["expected_output"]), msg=testcase)
            test_counter += 1

    def test_intersection_of_bounding_boxes(self):
        # intersection_of_bounding_boxes(box1, box2) -> box, if there's no intersection it returns None
        json_filename = json_path_prefix + "intersection_of_bounding_boxes.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            box_1 = box.Box(None, "Box_1",
                            cube.Cube(testcases[testcase]["box_1"]["length"], testcases[testcase]["box_1"]["height"],
                                      testcases[testcase]["box_1"]["width"]),
                            position.Position(testcases[testcase]["box_1"]["x"], testcases[testcase]["box_1"]["y"],
                                              testcases[testcase]["box_1"]["z"], 0, 0), None, None)
            box_2 = box.Box(None, "Box_2",
                            cube.Cube(testcases[testcase]["box_2"]["length"], testcases[testcase]["box_2"]["height"],
                                      testcases[testcase]["box_2"]["width"]),
                            position.Position(testcases[testcase]["box_2"]["x"], testcases[testcase]["box_2"]["y"],
                                              testcases[testcase]["box_2"]["z"], 0, 0), None, None)
            if testcases[testcase]["intersection_box"] == "None":
                self.assertIsNone(in_in.IntersectionInstance.intersection_of_bounding_boxes(box_1, box_2),
                                  msg=testcase)
            else:
                intersection_box = box.Box(None, "intersection_box",
                                           cube.Cube(testcases[testcase]["intersection_box"]["length"],
                                                     testcases[testcase]["intersection_box"]["height"],
                                                     testcases[testcase]["intersection_box"]["width"]),
                                           position.Position(testcases[testcase]["intersection_box"]["x"],
                                                             testcases[testcase]["intersection_box"]["y"],
                                                             testcases[testcase]["intersection_box"]["z"], 0, 0), None,
                                           None)
                with self.subTest(i=test_counter):
                    self.assertTrue(
                        teto.bounding_box_equal(
                            in_in.IntersectionInstance.intersection_of_bounding_boxes(box_1, box_2),
                            intersection_box), msg=testcase)
            test_counter += 1

    def test_cylinder_cube_intersection(self):
        json_filename = json_path_prefix + "cylinder_cube.json"
        with open(json_filename, "r") as f:
            testcases = json.load(f)
        test_counter = 0
        for testcase in testcases:
            with self.subTest(i=test_counter):
                cylinder_obj = object.Object(1, "Cylinder", cylinder.Cylinder(testcases[testcase]["cylinder"]["radius"],
                                                                              testcases[testcase]["cylinder"][
                                                                                  "height"]),
                                             position.Position(testcases[testcase]["cylinder"]["x"],
                                                               testcases[testcase]["cylinder"]["y"],
                                                               testcases[testcase]["cylinder"]["z"],
                                                               testcases[testcase]["cylinder"]["phi"],
                                                               testcases[testcase]["cylinder"]["theta"]), None, None)
                cube_obj = object.Object(1, "Cube",
                                         cube.Cube(testcases[testcase]["cube"]["length"],
                                                   testcases[testcase]["cube"]["height"],
                                                   testcases[testcase]["cube"]["width"]),
                                         position.Position(testcases[testcase]["cube"]["x"],
                                                           testcases[testcase]["cube"]["y"],
                                                           testcases[testcase]["cube"]["z"],
                                                           testcases[testcase]["cube"]["phi"],
                                                           testcases[testcase]["cube"]["theta"]), None, None)
                accuracy = testcases[testcase]["accuracy"]
                maximum_possible_volume_of_intersection = testcases[testcase]["maximum_possible_volume_of_intersection"]
                volume_of_intersection = testcases[testcase]["output"]["volume_of_intersection"]
                almost_zero = testcases[testcase]["almost_zero"]
                epsilon = testcases[testcase]["epsilon_for_point_of_intersection"]
                intersection_instance = in_in.IntersectionInstance(cylinder_obj, cube_obj, accuracy,
                                                                   maximum_possible_volume_of_intersection)
                intersection_point = testcases[testcase]["output"]["intersection_point"]
                # checking volume of intersection
                if volume_of_intersection > maximum_possible_volume_of_intersection:
                    # if the volume_of_intersection is non-infinitesimal, then the output must be in the range of non-infinitesimal too.
                    self.assertTrue(
                        (intersection_instance.get_volume_of_intersection() > maximum_possible_volume_of_intersection),
                        msg=testcase)
                    self.assertTrue(
                        teto.point_almost_equal(intersection_instance.get_intersection_point(), intersection_point,
                                                epsilon), msg=testcase)
                elif almost_zero < volume_of_intersection <= maximum_possible_volume_of_intersection:
                    # infinitesimal intersection
                    self.assertTrue(
                        0 < intersection_instance.get_volume_of_intersection() <= maximum_possible_volume_of_intersection,
                        msg=testcase)
                    self.assertTrue(teto.point_almost_equal(intersection_instance.get_intersection_point(),
                                                            intersection_point,
                                                            epsilon), msg=testcase)
                elif 0 <= volume_of_intersection <= almost_zero:
                    # infinitesimal intersection which can be interpreted as no intersection too
                    self.assertTrue(
                        0 <= intersection_instance.get_volume_of_intersection() <= maximum_possible_volume_of_intersection,
                        msg=testcase)
                    if intersection_instance.get_volume_of_intersection() != 0:
                        self.assertTrue(teto.point_almost_equal(intersection_instance.get_intersection_point(),
                                                                intersection_point,
                                                                epsilon), msg=testcase)
                    else:
                        self.assertEqual(len(intersection_instance.get_intersection_point()), 0)
                else:
                    # no intersection
                    self.assertAlmostEqual(intersection_instance.get_volume_of_intersection(), 0, msg=testcase)
                    self.assertEqual(len(intersection_instance.get_intersection_point()), 0)

            test_counter += 1

    def test_non_physical_object_intersection(self):
        pass


if __name__ == '__main__':
    unittest.main()
