from __future__ import annotations
from mongol import Mongol

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str
    age: int

result = Client.updateOne(filter={"name": "Van Andaime"}, data={"name": "Kombini"})
print(result.modified_count)

result = Client.updateMany(filter={"name": "Kombini"}, data={"name": "Van Andaime"})
print(result.modified_count)