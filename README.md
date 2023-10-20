# Mongol

Mongol is easy method to connect with interact to MongoDB.

## How to install

```sh
git clone https://github.com/brumazzi/mongol
cd mongol
pip install -r requirements.txt
pip install .
```

## How to use

```python
from __future__ import annotations
import mongol

Mongol = mongol.Mongol

Mongol.database = "testCollection"

class Client(Mongol):
    fields = {
        "name": "",
        "age": 0,
        "extra": {"if": "self['age'] < 18", "default": "Extra"}
    }

    validates = [
        {"field": "name", 'role': 'type', 'roleValue': str},
        {"field": "age", 'role': 'required', 'roleValue': True}
    ]

Client.destroyMany()

names = [
    ["Unonn", 19],
    ["Alpha", 14],
    ["Person", 18],
    ["Alpha", None],
    ["Laster", 20],
    ["Lancer", 19],
    [0, 7]
]

for name in names:
    c = Client(name= name[0], age = name[1])
    if c.isValid():
        c.save()
    else:
        print(c.errors)
    del c


for client in Client.find():
    print(client["_id"], client)
```
