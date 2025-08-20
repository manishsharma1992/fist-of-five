from dataclasses import dataclass
from typing import FrozenSet, Optional

from src.domain.auth.aggregate.entities import Role

@dataclass(frozen=True, slots=True)
class UpsertUserCmd:
    id: Optional[int]
    uid: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password_plain: Optional[str] = None
    role_ids: Optional[FrozenSet[int]] = None
    actor: str = "SYSTEM"