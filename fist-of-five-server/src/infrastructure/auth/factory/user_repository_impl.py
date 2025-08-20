from typing import Optional

from sqlalchemy import select

from src.domain.auth.repository.user_repository import UserRepository
from src.domain.auth.aggregate.entities import User
from src.infrastructure import SessionLocal
from src.infrastructure.auth.mappers.user_row_mapper import to_entity
from src.infrastructure.auth.orm.tables import UserRow


class UserRepositoryImpl(UserRepository):
    def __init__(self, session_factory=SessionLocal):
        self._sf = session_factory

    def by_id(self, user_id: int) -> Optional[User]:
        with self._sf() as s:
            row = s.get(UserRow, user_id)
            return to_entity(row) if row else None

    def by_uid(self, uid: str) -> User | None:
        with self._sf() as s:
            row = s.get(UserRow, uid)
            return to_entity(row) if row else None

    def list(self):
        with self._sf() as s:
            rows = s.execute(select(UserRow)).scalars().all()
            return [to_entity(r) for r in rows]

