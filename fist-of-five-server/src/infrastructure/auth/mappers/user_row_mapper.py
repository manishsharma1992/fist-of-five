from src.domain.common.value_objects import AuditStamp
from src.infrastructure.auth.orm.tables import UserRow
from src.domain.auth.aggregate.entities import User

def to_entity(row: UserRow) -> User:
    return User(
        id=row.id,
        uid=row.uid,
        first_name=row.first_name,
        last_name=row.last_name,
        username=row.username,
        password_hash=row.password,
        roles=row.roles,
        audit=AuditStamp(
            created_by=row.created_by,
            created_at=row.created_at,
            updated_by=row.updated_by,
            updated_at=row.updated_at
        )
    )

def apply_entity(row: UserRow, user: User) -> None:
    row.uid = user.uid
    row.first_name = user.first_name
    row.last_name = user.last_name
    row.username = user.username
    row.password = user.password_hash
    row.roles = user.roles
    row.created_by = user.audit.created_by
    row.created_at = user.audit.created_at
    row.updated_at = user.audit.updated_at
    row.updated_by = user.audit.updated_by