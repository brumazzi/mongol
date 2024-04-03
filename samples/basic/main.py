from __future__ import annotations
from mongol import Mongol, Validation

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str = Validation(required=True)
    age: int = Validation(min=18)
    _delete: bool

    def printChangesIfExists__BeforeSave(self):
        if not self.changes: return None
        print("=========")
        print(self.changes)
        print("=========")

    def printSuccess__AfterSave(self):
        print("Saved with success!")

    def canDelete__BeforeDelete(self):
        if self._delete != True:
            self.error = f"{self.__class__.__name__}", "Need check \"_delete\" with True to continue!"

    def success__AfterDelete(self):
        print("Delete success!")

    def invalidNames__Validation(self):
        if self.name.lower() in ["qwerty", "asdf"]:
            self.error = "name", f"Name can't be {self.name}"


################################################

client: Client = Client(name="Qwerty", age=16)

if not client.save():
    for error, message in client.errors.items():
        print(f"{error}: {message}")

print("------------------------------------")

client.name = "Person"
client.age = "25"

if not client.save():
    for error, message in client.errors.items():
        print(f"{error}: {message}")

client.age = 20

print("------------------------------------")

if not client.save():
    for error, message in client.errors.items():
        print(f"{error}: {message}")

id = client._id

del client

print("------------------------------------")

existsClient: Client = Client.findOne(filter={"_id": id}, format=object)
existsClient.update(name="Person Janckson")

print("------------------------------------")

if not existsClient.delete():
    for error, message in existsClient.errors.items():
        print(f"{error}: {message}")

print("------------------------------------")

existsClient._delete = True
existsClient.delete()