from __future__ import annotations

from pymongo import MongoClient
import inflection

from .partials import MongolField, MongolValidate

class Mongol(MongolField, MongolValidate):
    validation_errors: dict = dict()

    def __init__(self, **kwds):
        if not hasattr(self.__class__, "table"): self.__sync()

        self.initFields()
        self.populate(**kwds)
        self.start()

    @classmethod
    def find(self, **query) -> list:
        if not hasattr(self.__class__, "table"): self.__sync_class()
        registers = list()
        for data in self.table.find(query):
            registers.append(self(**data))
            registers[-1]["_id"] = str(registers[-1]["_id"])
        return registers

    @classmethod
    def findOne(self, **query) -> list:
        if not hasattr(self.__class__, "table"): self.__sync_class()
        self["_id"] = str(self["_id"])
        return self(**self.table.find_one(query))

    def start(self):
        pass

    def destroy(self):
        return self.table.delete_one({"_id": self["_id"]})

    @classmethod
    def destroyMany(self, **query):
        if not hasattr(self.__class__, "table"): self.__sync_class()
        return self.table.delete_many(query)

    def save(self, validation: str = True) -> bool:
        if validation:
            if not self.validate():
                return False
        for func in self.beforeSave:
            self.__getattribute__(func)()
        self["_id"] = str(self.table.insert_one(self.finalData()).inserted_id)
        for func in self.afterSave:
            self.__getattribute__(func)()
        return True

    @classmethod
    def __sync_class(self):
        self.connection = Mongol.connection
        if not hasattr(self, "table_name"):
            self.table_name = inflection.pluralize(inflection.underscore(self.__name__))
        self.collection = self.connection[Mongol.collection]
        self.table = self.collection[self.table_name]

    def __sync(self):
        self.connection = Mongol.connection
        if not hasattr(self, "table_name"):
            self.table_name = inflection.pluralize(inflection.underscore(self.__class__.__name__))
        self.collection = self.connection[Mongol.collection]
        self.table = self.collection[self.table_name]

    def __repr__(self):
        output = f"<{self.__class__.__name__}"
        for field in self.fields:
            output += f" @{field}='{self[field]}'"
        output += ">"
        return output

    def __str__(self):
        return self.__repr__()

    def __dict__(self):
        return dict(self)

def listen(host: str = "localhost", port: int = 27017):
    Mongol.connection = MongoClient(host, port)
Mongol.listen = listen