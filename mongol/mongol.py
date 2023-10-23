from __future__ import annotations

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from bson.objectid import ObjectId
import inflection

from .partials import MongolData, MongolValidate

class Mongol(MongolData, MongolValidate):
    database: str
    databaseConn: Database = None
    collection: Collection = None
    collectionName: str
    connection: MongoClient = None
    host: str = "127.0.0.1"
    port: int = 27017

    def __init__(self, **kwds):
        self.__populate__(**kwds)

    def __del__(self):
        self.__close_db__()

    def save(self, validation: bool = True) -> bool:
        self._sync_db_()
        if validation:
            if not self.validate(): return False
        for func in self.beforeSave: self.__getattribute__(func)()

        if self.get("_id"):
            result = self.collection.update_one({"_id": ObjectId(self["_id"])}, {"$set": self.dataToSave()})
            if result.matched_count == 0: return False
        else:
            result = self.collection.insert_one(self.dataToSave())
            if not result: return False
            self["_id"] = str(result.inserted_id)

        for func in self.afterSave: self.__getattribute__(func)()
        self.__close_db__()
        self.__update_dict_data__(**self.dataToSave())
        return True

    def update(self, **kwds):
        self.__populate__(**kwds)
        return self.save()

    def destroy(self) -> bool:
        self._sync_db_()
        result = self.collection.delete_one({"_id": ObjectId(self["_id"])})
        if result.deleted_count == 0:
            return False
        self.__close_db__()
        return True

    def _sync_db_(self):
        self.connection = MongoClient(Mongol.host, Mongol.port)
        self.databaseConn = self.connection[Mongol.database]
        self.collectionName = inflection.pluralize(inflection.underscore(self.__class__.__name__))
        self.collection = self.databaseConn[self.collectionName]

    @classmethod
    def __sync_db__(self, _class) -> Collection:
        connection = MongoClient(Mongol.host, Mongol.port)
        databaseConn = connection[Mongol.database]
        collectionName = inflection.pluralize(inflection.underscore(_class.__name__))
        return databaseConn[collectionName]

    @classmethod
    def findOne(self, filter={}, projection={}) -> Mongol | None:
        collection: Collection = Mongol.__sync_db__(self)
        if "_id" in filter: filter["_id"] = ObjectId(filter["_id"])

        register: dict = collection.find_one(filter, projection)

        collection.database.client.close()
        if not register: return None
        register["_id"] = str(register["_id"])
        return self(**register)

    @classmethod
    def find(self, filter={}, projection={}) -> list[Mongol]:
        collection: Collection = Mongol.__sync_db__(self)
        if "_id" in filter: filter["_id"] = ObjectId(filter["_id"])

        cursor: Cursor[self] = collection.find(filter, projection)
        registers: list[self] = list()
        for item in cursor:
            item["_id"] = str(item["_id"])
            registers.append(self(**item))

        collection.database.client.close()
        return registers

    def __close_db__(self):
        if self.connection: self.connection.close()

    def __repr__(self):
        output = f"<{self.__class__.__name__}"
        for field in self.fields:
            if self.get(field): output += f" @{field}='{self.get(field)}'"
        output += ">"
        return output

    def __str__(self):
        return self.__repr__()

    def __dict__(self):
        return dict(self)