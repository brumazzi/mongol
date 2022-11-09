from mongol import Mongol

Mongol.collection = "test-collection"
Mongol.listen()

class Client(Mongol):
    fields = {
            "name": {"type": str, "min": 5, "max": 30, "presence": True},
            "age": {"type": int, "min": 18, "default": 18},
            "extra": {"type": dict, "default": {"a":4, "b":5}}
    }

c = Client(name="One People")
if c.is_valid():
    c.save()
else:
    print(c.errors())

for client in Client.find():
    print(client)
