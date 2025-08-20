from dataclasses import dataclass
from typing import FrozenSet


@dataclass(frozen=True, slots=True)
class RegisterUserRequest:
    uid: str
    first_name: str
    last_name: str
    username: str
    password: str          # plain from UI (HTTPS)
    role_ids: FrozenSet[int]
    actor: str # who is performing action

@dataclass(frozen=True, slots=True)
class UserResponse:
    id: int
    uid: str
    username: str
    first_name: str
    last_name: str
    roles: list[str]