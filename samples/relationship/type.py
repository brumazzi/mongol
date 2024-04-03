from __future__ import annotations
from mongol import Mongol, Validation, ReferenceCollection

@ReferenceCollection
class Type(Mongol):
    name: str
    category: str
    user_id: Reference[__main__.Client]
    client_id: Reference[__main__.Client]