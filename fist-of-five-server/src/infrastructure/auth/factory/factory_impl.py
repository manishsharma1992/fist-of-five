from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.domain.auth.commands.commands import UpsertUserCmd
from src.domain.auth.ports.ports import UserFactory
from src.domain.auth.aggregate.entities import User
from src.infrastructure import SessionLocal
from src.infrastructure.auth.mappers.user_row_mapper import to_entity
from src.infrastructure.auth.orm.tables import UserRow, RoleRow


class UserFactory(UserFactory):
    def __int__(self, session_factory=SessionLocal):
        self._sf = session_factory

    def create(self, cmd: UpsertUserCmd) -> User:
        """
        Persist a new user with role_ids resolved to RoleRow and return the domain User.
        Assumes:
          - UserRow.password_hash exists (not plaintext)
          - UserRow has created_by/created_at/updated_by/updated_at columns
          - Many-to-many via user_roles is configured
        """
        with self._sf() as s:
            now = datetime.now(timezone.utc)

            # 1) Resolve role IDs -> RoleRow
            role_rows = []
            if cmd.role_ids:
                role_rows = (
                    s.execute(select(RoleRow).where(RoleRow.id.in_(list(cmd.role_ids))))
                    .scalars()
                    .all()
                )
                missing = set(cmd.role_ids) - {r.id for r in role_rows}
                if missing:
                    raise ValueError(f"Unknown role ids: {sorted(missing)}")

            # 2) Create the UserRow; attach roles and audit fields
            row = UserRow(
                uid=cmd.uid,
                first_name=cmd.first_name,
                last_name=cmd.last_name,
                username=cmd.username,
                password=cmd.password_plain,  # already hashed upstream
                created_by=cmd.actor,
                created_at=now,
                updated_by=cmd.actor,
                updated_at=now,
            )
            row.roles = role_rows  # many-to-many

            s.add(row)
            s.flush()      # materialize generated PK
            s.refresh(row) # ensure defaults/identity are loaded
            s.commit()

            # 3) Reload with roles eagerly for clean mapping
            row = (
                s.execute(
                    select(UserRow)
                    .options(selectinload(UserRow.roles))
                    .where(UserRow.id == row.id)
                )
                .scalar_one()
            )

            return to_entity(row)