from __future__ import annotations
import object

ObjectId = int


class ObjectRegistry:
    def __init__(self):
        self.__objects: dict[ObjectId, object.Object] = {}
        self.__next_available_id = 0

    def get_objects(self) -> dict[ObjectId, object.Object]:
        """
        Returns the dictionary self.__objects with ObjectIDs as keys and Objects as values.
        """
        return self.__objects

    def add_objects(self, new_objects: dict[ObjectId, object.Object]) -> None:
        """Updates the dictionary of objects.

        Args:
            new_objects: Will be added to self.__objects
        """
        self.__objects.update(new_objects)

    def get_next_available_id(self) -> ObjectId:
        """
        Returns the next available id.
        """
        self.__next_available_id += 1
        return self.__next_available_id
