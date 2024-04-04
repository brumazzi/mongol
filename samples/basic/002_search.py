from __future__ import annotations
from mongol import Mongol

Mongol.DATABASE = "testDatabase"

class Client(Mongol):
    name: str
    age: int

client: Client = Client.findOne(filter={}, format=object) # convert data to Client object
print(client.name, client)
del client

clientDict: dict = Client.findOne()
print(clientDict["name"], clientDict)
del clientDict

for client in Client.find(format=object):
    print(client.name, client)

for clientDict in client.find():
    print(clientDict["name"], clientDict)