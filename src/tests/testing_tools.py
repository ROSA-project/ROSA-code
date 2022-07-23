import numpy as np
from box import Box
from box import Box

radians_accuracy_decimal_points = 10
real_number_accuracy_decimal_points = 8


def angle_almost_equal(angle1: float, angle2: float):
    modulo_value = 360
    return round(angle1 % modulo_value - angle2 % modulo_value, \
                 radians_accuracy_decimal_points) == 0


def matrix_almost_equal(matrix1: list, matrix2: list):
    """
        input matrices being nested lists. We use np.array to be able to do 
        element wise subtraction.
        input matrices can be numpy arrays too. second conversion is okay apparently
        import to support normal list as the expected matrix read from json is a list
    """
    np_matrix1 = np.array(matrix1)
    np_matrix2 = np.array(matrix2)

    if np_matrix1.size == 0 and np_matrix2.size == 0:
        return True

    return np.round(np.amax(abs(np_matrix1 - np_matrix2)), \
                    real_number_accuracy_decimal_points) == 0


def bounding_box_equal(box1: Box, box2: Box):
    if box1.position.x == box2.position.x and box1.position.y == box2.position.y and box1.position.z == box2.position.z and box1.position.phi == box2.position.theta:
        if box1.shape.length == box2.shape.length and box1.shape.height == box2.shape.height and box1.shape.width == box2.shape.width:
            return True
        else:
            return False
    else:
        return False
