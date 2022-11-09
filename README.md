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
from mongol import Mongol

# set database name
Mongol.collection = "test-collection"
# start connection with mongo db
Mongol.listen()

# create client table
class Client(Mongol):
    fields = {
            "name": {"type": str, "min": 5, "max": 30, "presence": True},
            "age": {"type": int, "min": 18, "default": 18},
            "extra": {"type": dict, "default": {"a":4, "b":5}}
    }

c = Client(name="One people")
if c.is_valid():
    c.save()

for client in Client.find():
    print(client)
```