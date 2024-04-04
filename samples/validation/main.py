from __future__ import annotations
from mongol import Mongol, Validation

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str = Validation(required=True, min=4, max=20)
    age: int = Validation(required=True,min=18,max=160, default=10)

    def checkName__Validation(self):
        if self.name.startswith("_"):
            # when set a list to error, the current error was appended
            # to errors stack
            self.error = "name", "cannot start with '_'!"

client: Client = Client(name="_Van Andaime Pereira da Silva dos Santo de Souza Farias de Guarapé")

if not client.save():
    for error in client.errors.items():
        print(error)