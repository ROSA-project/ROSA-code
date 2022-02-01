import object

class Map:
    """Handles reading/parsing/load of the map. Meant to be instantiated along the World
       and passed to it as input to its constructor.
    """
    def parse_map(filename: str): -> dict[oid: ObjectId, Object]
        pass