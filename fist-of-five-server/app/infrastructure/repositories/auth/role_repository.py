from typing import FrozenSet, Optional
from app.domain import Role
from sqlalchemy.orm import Session


class RoleRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self) -> frozenset[type[Role]]:
        roles = self.db.query(Role).all()
        return frozenset(roles)

    def find_by_name(self, name: str) -> Optional[Role]:
        """
        Find role by name.
        More efficient than fetching all roles.
        """
        return self.db.query(Role).filter_by(name=name).first()