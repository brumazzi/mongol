from __future__ import annotations
from mongol import Mongol

from type import Type
from permission import Permission
from user import User

Mongol.DATABASE = "testDatabase"

Permission.deleteMany()
Type.deleteMany()
User.deleteMany()

for permissionName in "read,write,create,delete".split(","):
    Permission.insert(name=permissionName, description=f"can permit {permissionName} action")

for typeName in "admin,user,visitor".split(","):
    Type.insert(name=typeName)

user = User(name="Admin", email="admin@admin.com")
user.permission_ids = [ permission._id for permission in Permission.find(format=object, filter={"name": {"$in": ["read", "write", "create"]}}) ]
user.type_id = Type.findOne(filter={"name": "admin"}, format=object)._id
user.save()

print(user.type.name)
for permission in user.permissions:
    print(permission.name)

print(User.findOne(filter={"_id": user._id}, recursiveLevel=2))