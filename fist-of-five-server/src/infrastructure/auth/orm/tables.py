from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Identity, Integer, String, Table
from sqlalchemy.orm import relationship

from src.infrastructure import db

SCHEMA = "planning_poker"

# Join table for many-to-many relationship between User and Role
user_roles = Table(
    'user_roles',
    db.metadata,
    Column('user_id', ForeignKey(f"{SCHEMA}.users.id"), primary_key=True),
    Column('role_id', ForeignKey(f"{SCHEMA}.roles.id"), primary_key=True),
    schema=SCHEMA
)

# Join table for many-to-many relationship between Role and Permission
role_permissions = Table(
    'role_permissions',
    db.metadata,
    Column("role_id", ForeignKey(f"{SCHEMA}.roles.id"), primary_key=True),
    Column('permission_id', ForeignKey(f"{SCHEMA}.permissions.id"), primary_key=True),
    schema=SCHEMA
)


class UserRow(db.Model):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, Identity(), primary_key=True)
    uid = db.Column(db.String(6), unique=True, nullable=False)
    first_name = db.Column(db.String(126), nullable=False)
    last_name = db.Column(db.String(126), nullable=False)
    username = db.Column(db.String(126), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_by = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Establish many-to-many relationship with Role
    roles = relationship(
        'RoleRow',
        secondary=user_roles,
        lazy='selectin',
        backref=db.backref('users', lazy="selectin"))

    def __repr__(self):
        return f"<UserRow {self.username}>"


class RoleRow(db.Model):
    __tablename__ = "roles"
    __table_args__ = {"schema": SCHEMA}

    id = db.Column(Integer, Identity(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(50), nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_by = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # relationships
    users = relationship(  # backref from UserRow.roles handles this; keeping for clarity
        "UserRow",
        secondary=user_roles,
        lazy="selectin",
        viewonly=True,
    )
    permissions = relationship(
        "PermissionRow",
        secondary=role_permissions,
        lazy="selectin",
        backref=db.backref("roles", lazy="selectin"),
    )

    def __repr__(self):
        return f"<RoleRow {self.name}>"


class PermissionRow(db.Model):
    __tablename__ = "permissions"
    __table_args__ = {"schema": SCHEMA}

    id = db.Column(Integer, Identity(), primary_key=True)
    name = db.Column(String(50), unique=True, nullable=False)
    description = db.Column(String(255), nullable=False)

    created_by = db.Column(String(50), nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_by = db.Column(String(50), nullable=False)
    updated_at = db.Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # backref from RoleRow.permissions supplies .roles

    def __repr__(self):
        return f"<PermissionRow {self.name}>"
