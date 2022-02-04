class Shape:
    def __init__(self):
        pass
    
    def bounding_box(self):
        """Returns the x-y plane bounding box for the shape
        """
        pass

    def is_empty(self) -> bool:
        """ Shape is not "empty" if it has nonzero volumn or nonzero area
        """
        return False

class VoidShape(Shape):
    def is_empty(self) -> bool:
        """overwriting parent method
        """
        return True