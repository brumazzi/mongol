# Mongol

Mongol is easy method to connect with interact to MongoDB.

## How to install

```sh
git clone https://github.com/brumazzi/mongol
cd mongol
pip install -r requirements.txt
pip install .
```

## How to use

```python
from __future__ import annotations
from mongol import Mongol

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str
    age: int
    _delete: bool

    def printChangesIfExistsBeforeSave(self):
        if not self.changes: return None
        print("=========")
        print(self.changes)
        print("=========")

    def printSuccess__AfterSave(self): # can add underscore to separe callback type
        print("Saved with success!")

    def canDelete__BeforeDelete(self):
        if self._delete != True:
            self.error = {f"{self.__class__.__name__}": "Need check \"_delete\" with True to continue!"}

    def success__AfterDelete(self):
        print("Delete success!")

    def minAgeValidation(self):
        if type(self.age) is int and self.age < 18:
            self.error = {"age": "Age needed be greater then 18 to register!"}

    def invalidNames__Validation(self): # can add underscore to separe callback type
        if self.name.lower() in ["qwerty", "asdf"]:
            self.error = {"name": f"Name can't be {self.name}"}


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
```
