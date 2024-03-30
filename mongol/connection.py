from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import inflection

from bson.objectid import ObjectId


class Connection(MongoClient):
    database: Database = None
    collection: Collection = None
    mongol: any = None

    def __init__(self, mongol: any):
        className = mongol.__class__.__name__
        if mongol.__class__ == type:
            className = mongol.__name__

        collectionName = inflection.pluralize(inflection.underscore(className))

        super().__init__(mongol.HOST, mongol.PORT)

        self.database = self[mongol.DATABASE]
        self.collection = self.database[collectionName]
        if mongol.__class__ != type:
            self.mongol = mongol
            self.mongol.connection = self

    def __del__(self):
        if self.mongol: self.mongol.connection = None
        try: self.close()
        except: pass


# connection decorators
def db_connect(callback):
    def layer(self=None, *args, **kwds):
        conn = Connection(self)
        response = callback(self, *args, **kwds)
        del conn

        return response
    return layer

class MorphicCollection:
    collection: Collection

    def __init__(self, connection: Connection, collection: str):
        self.collection = connection.database[inflection.pluralize(inflection.underscore(collection))]

    def find(self, id: str|ObjectId) -> dict:
        return self.collection.find_one({"_id": ObjectId(id)})