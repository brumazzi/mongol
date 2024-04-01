from __future__ import annotations

from pymongo.cursor import Cursor
from bson.objectid import ObjectId
from mongol.connection import db_connect, Connection, MorphicCollection
from mongol.validation import Validation, DataValidation
from mongol.automation import run_before_after

import re

QUERY_FORMAT_DICT   = dict
QUERY_FORMAT_OBJECT = object

def matchRecursiveID(data: dict):
    for key, value in data.items():
        if type(value) is dict: matchRecursiveID(value)
        elif not re.sub("(\\w.+_id|_id)", "", key):
            data[key] = ObjectId(data[key])

def openReferenceTree(data: dict, connection: Connection, recursiveLevel=1):
    if recursiveLevel == 0: return

    for key, value in data.items():
        if type(value) is list:
            for v in value:
                if type(value) is dict: openReferenceTree(value, connection, recursiveLevel-1)
        if type(value) is dict:
            openReferenceTree(value, connection, recursiveLevel-1)
        if not re.sub("\\w.+_id", "", key) and value:
            collectionName: str = key[:-3]

            morth = MorphicCollection(connection, collectionName)
            result = morth.find(value)
            data[key] = result

            openReferenceTree(result, connection, recursiveLevel-1)
        if not re.sub("\\w.+_ids", "", key):
            collectionName: str = key[:-4]
            dataList: list = list()

            for v in value:
                morth = MorphicCollection(connection, collectionName)
                result = morth.find(v)
                dataList.append(result)

                openReferenceTree(result, connection, recursiveLevel-1)
            data[key] = dataList

class Query():
    @classmethod
    def find(self, format=dict, filter={}, projection={}, recursiveLevel=1, **kwds) -> list[dict|any]:
        matchRecursiveID(filter)
        conn = Connection(self)
        cursor: Cursor[self] = conn.collection.find(filter, projection, **kwds)

        if format == object:
            data: list = list()
            for item in cursor:
                mongol = self(**item)
                mongol._db_data = item
                mongol._db_data_before_save = mongol._db_data
                data.append(mongol)
        else:
            data = [ dict(item) for item in cursor ]
            for d in data:
                openReferenceTree(d, conn, recursiveLevel)

        del conn
        return data

    @classmethod
    def findOne(self, format=dict, filter={}, projection={}, recursiveLevel=1, **kwds) -> dict|any:
        matchRecursiveID(filter)
        conn = Connection(self)
        data = conn.collection.find_one(filter, projection, **kwds)
        del conn

        if format == object:
            mongol = self(**data)
            mongol._db_data = data
            mongol._db_data_before_save = mongol._db_data
            return mongol

        openReferenceTree(data, conn, recursiveLevel)
        return data

    @classmethod
    def updateOne(self, filter={}, data={}, **kwds):
        matchRecursiveID(filter)
        conn = Connection(self)
        res = conn.collection.update_one(filter, {"$set": data}, **kwds)
        del conn
        return res

    @classmethod
    def updateMany(self, filter={}, data={}, **kwds):
        matchRecursiveID(filter)
        conn = Connection(self)
        res = conn.collection.update_many(filter, {"$set": data}, **kwds)
        del conn
        return res

    @classmethod
    def deleteOne(self, filter={}, **kwds):
        matchRecursiveID(filter)
        conn = Connection(self)
        res = conn.collection.delete_one(filter, **kwds)
        del conn
        return res

    @classmethod
    def deleteMany(self, filter={}, **kwds):
        matchRecursiveID(filter)
        conn = Connection(self)
        res = conn.collection.delete_many(filter, **kwds)
        del conn
        return res

class Data(DataValidation):

    def save(self, skipValidate=False) -> bool:
        if not skipValidate:
            if not self.validate():
                return False
        self.__save()

    @run_before_after("save")
    @db_connect
    def __save(self) -> bool:
        saveData = {}
        for field in self.fields:
            if not field.startswith("_"):
                saveData[field] = self.__getattribute__(field)

        if not self._db_data_before_save:
            self._db_data_before_save = self.data

        if self._id:
            result = self.collection.update_one({"_id": self._id}, {"$set": saveData})
        else:
            result = self.collection.insert_one(saveData)
            self._id = ObjectId(result.inserted_id)
        self._db_data = self.data

        return result.acknowledged

    def update(self, skipValidate=False, **kwds):
        for key in kwds.keys(): self.__setattr__(key, kwds.get(key))
        return self.save(skipValidate=skipValidate)

    def delete(self) -> bool:
        self._errors = {}
        return self.__delete()

    @run_before_after("delete")
    @db_connect
    def __delete(self) -> bool:
        if not self._id or self.errors: return False

        self.collection.delete_one({"_id": self._id})
        return True

    @run_before_after("validate")
    def validate(self) -> bool:
        self.runValidations()
        if len(self.errors) > 0: return False
        return True

    @property
    def changes(self) -> dict:
        if self.isNew: return {}

        setObject: set = set(self.data.items())
        setDB: set = set(self.dataDB.items())

        setDiff: set = setObject ^ setDB

        result = dict()
        for data in setDiff:
            if not data[0] in result: result[data[0]] = [None, None]

            if data[1] == self.__getattribute__(data[0]):
                result[data[0]][1] = data[1]
            else:
                result[data[0]][0] = data[1]

        return result

    @property
    def changesAfterSave(self) -> dict:
        if self.isNew: return {}

        setObject: set = set(self.data.items())
        setDB: set = set(self.dataDBChanged.items())

        setDiff: set = setObject ^ setDB

        result = dict()
        for data in setDiff:
            if not data[0] in result: result[data[0]] = [None, None]

            if data[1] == self.__getattribute__(data[0]):
                result[data[0]][1] = data[1]
            else:
                result[data[0]][0] = data[1]

        return result

    @property
    def data(self) -> dict:
        return { k: self.__getattribute__(k) for k in self.fields }

    @property
    def dataDB(self) -> dict:
        return { k: self._db_data.get(k) for k in self.fields }

    @property
    def dataDBChanged(self) -> dict:
        print(self._db_data)
        return { k: self._db_data_before_save.get(k) for k in self.fields }

    @property
    def fields(self) -> list:
        return [ k for k in self.__annotations__.keys() if not k.startswith("_") ]

    @property
    def isNew(self) -> bool:
        return self._id == None