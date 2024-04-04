from __future__ import annotations
from mongol import Mongol

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str
    age: int

client: Client = Client(name="Van Andaime", age=56)

if client.save():
    print("Success!")