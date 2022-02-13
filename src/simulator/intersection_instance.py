class IntersectionInstance:
    """performs intersection between two objects and stores the result. 
       A primary result is a shape.
    """
    def __init__(self, object1, object2):
        self.object1 = object1
        self.object2 = object2
        self.result = self.intersect()

    def intersect(self) -> dict:
        """ performs the intersection algorithm on its two objects, and returns what?!

        Returns:
            not clear for now, as it's not clear what information we need.
            Returns None if no intersection.
        """
        # TODO to be implemented, this is a placeholder
        return None

    