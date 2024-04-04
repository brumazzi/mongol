from __future__ import annotations
from mongol import Mongol

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str
    age: int

result = Client.deleteOne(filter={"name": "Van Andaime"})
print(result.deleted_count)

result = Client.deleteMany(filter={"age": 16})
print(result.deleted_count)