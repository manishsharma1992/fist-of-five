from typing import Protocol

from src.domain.auth.commands.commands import UpsertUserCmd
from src.domain.auth.aggregate.entities import User


class UserFactory(Protocol):
    def create_user(self, *, uid: str, first_name: str, last_name: str,
                    username: str, password_hash: str,
                    role_ids: frozenset[int], actor: str) -> User: ...