
from __future__ import annotations
from mongol import Mongol, Validation

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str = Validation(required=True, min=4, max=20)
    age: int = Validation(required=True,min=18,max=160, default=10)
    type: str
    _delete: bool

    def correctName__BeforeValidate(self):
        self.name = "Van Andaime"

    def setType__BeforeSave(self):
        self.type = "normal"

    def confirmSaveAndDelete__AfterSave(self):
        print("Client saved!", self)
        self.delete()

    def checkIfCanDelete__BeforeDelete(self):
        if self._delete != True:
            self.error = "_delete", "needed be True to delete this object!"

    def confirmDeletion__AfterDelete(self):
        print("Client deleted!")

    def checkName__Validation(self):
        if self.name.startswith("_"):
            self.error = "name", "cannot start with '_'!"

client: Client = Client(name="_Van Andaime Pereira da Silva dos Santo de Souza Farias de Guarapé", age=32)

client.save()

print(client.errors)
print("setting True to _delete")

client._delete = True
client.delete()