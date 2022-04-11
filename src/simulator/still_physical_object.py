import object


class StillPhysicalObject(object.Object):
    """
    A physical object that cannot move by assumption, even in absence of friction
    """

    def evolve(self,delta_t: float):
        pass