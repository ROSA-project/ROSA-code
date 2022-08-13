from object import Object

RadioID = str


class Base(Object):
    def __int__(self, oid, name, shape, position, owner_object, registry, rid: RadioID):
        super().__init__(oid, name, shape, position, owner_object, registry)
        self.radio_id = rid
