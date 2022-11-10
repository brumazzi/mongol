import mongol

Mongol = mongol.Mongol

Mongol = mongol.Mongol
Mongol.collection = "test-collection"
Mongol.listen()

class Client(Mongol):
    fields = {
            "name": {"type": str, "min": 5, "max": 30, "presence": True, "unique": True},
            "age": {"type": int, "min": 18, "default": 27},
            "extra": {"type": dict, "default": {"a":4, "b":5}}
    }

names = [
    "Unonn",
    "Alpha",
    "Person",
    "Alpha",
    "Laster",
    "Lancer"
]

for name in names:
    c = Client(name= name)
    if c.is_valid():
        c.save()
    else:
        print(c.errors())
    del c

print()

for client in Client.find():
    print(client)