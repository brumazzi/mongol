from __future__ import annotations
from mongol import Mongol

class Permission(Mongol):
    name: str
    description: str