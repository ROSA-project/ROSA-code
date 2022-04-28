import numpy as np

radians_accuracy_decimal_points = 10
real_number_accuracy_decimal_points = 10

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
    np_matrix1=np.array(matrix1)
    np_matrix2=np.array(matrix2)
    return np.round(np.amax(abs(np_matrix1-np_matrix2)),\
        real_number_accuracy_decimal_points) == 0
