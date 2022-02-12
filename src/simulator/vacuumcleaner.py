from robot import Robot


class VacuumCleaner(Robot):
    def __init__(self, id: ObjectId, shape: Shape, position: Position, owner_object):
        super().__init__()

    def evolve(self, delta_t: int, intersection_result) -> dict[ObjectId, Object]:
        # TODO type of intersection result
        # TODO saeed: could this be the default evolve method?
        collected_offspring_objects = []

        for object in self.dependent_objects:
            offspring_objects = object.evolve(delta_t, intersection_result)
            collected_offspring_objects.extend(offspring_objects)

        self.dependent_objects.extend(collected_offspring_objects)
        return collected_offspring_objects
