from __future__ import annotations
import object

# ObjectId = int


class ObjectRegistry:
    def __init__(self):
        self.__objects: dict[object.ObjectId, object.Object] = {}
        self.__next_available_id = 0

    def get_objects(self) -> dict[object.ObjectId, object.Object]:
        """
        Returns the dictionary of all current objects with ObjectIDs as keys and Objects as values.
        """
        return self.__objects

    def add_objects(self, new_objects: dict[object.ObjectId, object.Object]) -> None:
        """Updates the dictionary of objects.

        Args:
            new_objects: Will be added to the dictionary of all objects
        """
        self.__objects.update(new_objects)

    def get_next_available_id(self) -> object.ObjectId:
        """
        Returns the next available id.
        """
        self.__next_available_id += 1
        return self.__next_available_id
