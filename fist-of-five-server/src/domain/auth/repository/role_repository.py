from typing import Protocol
from src.domain.auth.aggregate.entities import Role

class RoleRepository(Protocol):
    def by_ids(self, ids: frozenset[int]) -> frozenset[Role]: ...