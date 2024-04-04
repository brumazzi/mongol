from __future__ import annotations

from mongol import Mongol, ReferenceCollection
"""
    To build relationship between collection it is mandatory that import annotation from __future__ package
    and use @ReferenceCollection decorator to configure relationships
"""

@ReferenceCollection
class User(Mongol):
    name: str
    email: str
    permission_ids: Reference[permission.Permission]
    type_id: Reference[type.Type]