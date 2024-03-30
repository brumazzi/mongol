from __future__ import annotations

from .connection import Connection
from .data import Data, Query
from .automation import Automation
from pymongo.collection import Collection

from bson.objectid import ObjectId

class Mongol(Query, Data, Automation):
    HOST: str = "127.0.0.1"
    PORT: int = 27017
    DATABASE: str = ""
    connection: Connection = None

    _errors: dict = None
    _before_deletes: list = None
    _after_deletes: list = None
    _before_saves: list = None
    _after_saves: list = None
    _before_validates: list = None
    _after_validates: list = None
    _validations: list = None

    _id: ObjectId = None
    _db_data: dict = None
    _db_data_before_save: dict = None

    def __init__(self, **kwds):
        if self.__class__ == Mongol:
            raise "Mongol can not be instantiated"

        self._errors = {}
        self._before_creates = []
        self._after_creates = []
        self._before_deletes = []
        self._after_deletes = []
        self._before_saves = []
        self._after_saves = []
        self._before_validates = []
        self._after_validates = []
        self._validations = []
        self._id = None
        self._db_data = None
        self._db_data_before_save = None
        self.syncMethods()

        for field in self.__annotations__:
            self.__setattr__(field, None)

        for key in kwds.keys():
            if key == "_id":
                self.__setattr__(key, ObjectId(kwds.get(key)))
            else:
                self.__setattr__(key, kwds.get(key))
        pass

    @property
    def collection(self) -> Collection:
        return self.connection.collection

    def __repr__(self):
        output = f"<{self.__class__.__name__}:{self._id}"
        for field in self.__annotations__.keys():
            if field.startswith("_"): continue
            elif not self.__getattribute__(field): continue
            output += f" @{field}='{self.__getattribute__(field)}'"
        output += ">"
        return output

    def __str__(self):
        return self.__repr__()