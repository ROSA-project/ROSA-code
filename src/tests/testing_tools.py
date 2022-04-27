radians_accuracy_decimal_points = 10

def angle_almost_equal(angle1: float, angle2: float):
    modulo_value = 360
    return round(angle1 % modulo_value - angle2 % modulo_value, \
        radians_accuracy_decimal_points) == 0