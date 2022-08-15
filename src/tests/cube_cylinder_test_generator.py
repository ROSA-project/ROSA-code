import math
import json

json_path_prefix = "src/tests/"


class CubeCylinderTestGenerator():
    """
    The calculations for cube_cylinder_intersection and the related testcase file are written here.
    Attributes:
    input_file_name: the name of the json file which has the initial data of the testcases
    output_file_name: the name or the json output file which includes the generated testcases
    """

    def __int__(self, input_file_name: str, output_file_name):
        self.input_file_address = input_file_name
        self.output_file_address = output_file_name
        self.generate_testcases()

    @staticmethod
    def volume_of_intersection_for_zero_theta_cube_corner(distance_between_center_and_corner: float,
                                                          radius_of_cylinder: float,
                                                          intersection_height: float) -> float:
        # TODO: add comments
        delta = (2 * (radius_of_cylinder ** 2)) - (distance_between_center_and_corner ** 2)
        half_of_the_diameter_of_intersection_square = (-distance_between_center_and_corner + math.sqrt(delta)) / 2
        length_of_intersection_square_edge = math.sqrt(2) * half_of_the_diameter_of_intersection_square
        volume = length_of_intersection_square_edge * length_of_intersection_square_edge * intersection_height
        return volume

    @staticmethod
    def original_intersection_point_for_zero_theta_cube_corner() -> [float, float, float]:
        # TODO: implement this
        pass

    @staticmethod
    def volume_of_intersection_for_zero_theta_cube_side(length_of_cube: float, radius_of_cylinder: float,
                                                        distance_of_center_and_corner: float,
                                                        intersection_height: float) -> float:
        # note that in this case the distance of center and corner is the delta x of these two points
        intersection_length = ((length_of_cube / 2) + radius_of_cylinder) - distance_of_center_and_corner
        intersection_width = 2 * math.sqrt(2 * radius_of_cylinder * intersection_length - (intersection_length ** 2))
        volume = intersection_length * intersection_width * intersection_height
        return volume

    @staticmethod
    def original_intersection_point_for_zero_theta_cube_side() -> [float, float, float]:
        # TODO: implement this
        pass

    def generate_testcases(self):
        tests = {}
        json_test_generator_file_name = json_path_prefix + self.input_file_address
        json_generated_tests_file_name = json_path_prefix + self.output_file_address
        test_counter = 0
        with open(json_test_generator_file_name, "r") as f:
            generators = json.load(f)
        for generator in generators:
            if generators[generator]["type"] == "zero_theta_cube_corner":
                volume = self.volume_of_intersection_for_zero_theta_cube_corner(
                    generators[generator]["distance_between_center_and_corner"],
                    generators[generator]["testcase"]["cylinder"]["radius"],
                    generators[generator]["intersection_height"])
                intersection_point = self.original_intersection_point_for_zero_theta_cube_corner()
                test = generators[generator]["testcase"]
                test["output"] = {"volume": volume, "intersection_point": intersection_point}
            elif generators[generator]["type"] == "zero_theta_cube_side":
                volume = self.volume_of_intersection_for_zero_theta_cube_side(
                    generators[generator]["testcase"]["cube"]["length"],
                    generators[generator]["testcase"]["cylinder"]["radius"],
                    generators[generator]["distance_of_center_and_corner"],
                    generators[generator["intersection_height"]])
                intersection_point = self.original_intersection_point_for_zero_theta_cube_side()
            else:
                raise "Unknown type of test generator!"

            test = generators[generator]["testcase"]
            test["output"] = {"volume": volume, "intersection_point": intersection_point}
            tests["t_" + str(test_counter)] = test
            test_counter += 1
        with open(json_generated_tests_file_name, "w") as tests_file:
            json.dump(tests, tests_file)
