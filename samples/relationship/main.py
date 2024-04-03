from __future__ import annotations
from mongol import Mongol, Validation, ReferenceCollection
from type import Type
from mongol.utils import classFromModule

import sys

# print(classFromModule('type.Type'))

Mongol.DATABASE = "testDatabase"

@ReferenceCollection
class Client(Mongol):
    name: str
    age: int
    type_id: Reference[type.Type]

    type_ids: Reference[type.Type]
    _delete: bool

t1 = Type(name="Test 1", category="One")
t1.save()
t2 = Type(name="Test 2", category="Two")
t2.save()
t3 = Type(name="Test 3", category="Three")
t3.save()

c = Client(name="Test", age=20)
c.type_id = t1._id
# c.type_ids = [t2._id, t3._id]
print(c.save())
# print(c.errors)

t1.client_id = c._id
t1.user_id = c._id
t1.save()

# print(c.type(format=dict))
print(Client.find(recursiveLevel=2))
print(t1.user())
# print(c.type.object)

# print(c.types[1].object)

# print(Client.find(recursiveLevel=2))

# print(t1.client.object)

Type.deleteMany()
Client.deleteMany()