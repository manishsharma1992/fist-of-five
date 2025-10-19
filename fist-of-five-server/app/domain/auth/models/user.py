from datetime import datetime, UTC

from sqlalchemy import Table, Column, BigInteger, ForeignKey, String, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship

from app.infrastructure.database.base import Base

SCHEMA = "agile_scrum"

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey(f"{SCHEMA}.users.id", ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey(f"{SCHEMA}.roles.id", ondelete='CASCADE'), primary_key=True),
    schema=SCHEMA
)

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    uid = Column(String(6), unique=True, nullable=False, index=True)
    email = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    active = Column(Boolean, default=True, nullable=False)

    created_by = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    modified_by = Column(BigInteger, nullable=True)
    modified_at = Column(DateTime, default=datetime.now(UTC), nullable=False)

    roles = relationship(
        "Role",
        secondary=user_roles,
        backref="users",
        lazy="joined"
    )

    def __repr__(self):
        return f"<User(uid='{self.uid}', email='{self.email}')>"
