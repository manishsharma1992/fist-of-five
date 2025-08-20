from dataclasses import dataclass, replace
from typing import Optional, FrozenSet, Set

from src.domain.common.value_objects import AuditStamp

@dataclass(frozen=True, slots=True)
class Permission:
    id: Optional[int]
    name: str
    description: str
    audit: AuditStamp


@dataclass(frozen=True, slots=True)
class Role:
    id: Optional[int]
    name: str
    description: str
    audit: AuditStamp
    permissions: FrozenSet[Permission] = frozenset()


@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    id: int
    uid: str
    first_name: str
    last_name: str
    username: str
    password_hash: str
    audit: AuditStamp
    roles: FrozenSet[Role] = frozenset()

    # withers – pass actor explicitly
    def with_first_name(self, *, first_name: str, actor: str) -> "User":
        return replace(self, first_name=first_name, audit=self.audit.touch(actor))

    def with_last_name(self, *, last_name: str, actor: str) -> "User":
        return replace(self, last_name=last_name, audit=self.audit.touch(actor))

    def with_uid(self, *, uid: str, actor: str) -> "User":
        return replace(self, uid=uid, audit=self.audit.touch(actor))

    def with_username(self, *, username: str, actor: str) -> "User":
        return replace(self, username=username, audit=self.audit.touch(actor))

    def with_password_hash(self, *, password_hash: str, actor: str) -> "User":
        return replace(self, password_hash=password_hash, audit=self.audit.touch(actor))

    def with_roles(self, *, roles: FrozenSet[Role], actor: str) -> "User":
        return replace(self, roles=roles, audit=self.audit.touch(actor))
