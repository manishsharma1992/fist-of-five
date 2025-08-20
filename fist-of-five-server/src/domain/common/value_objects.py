from dataclasses import dataclass, replace
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class AuditStamp:
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime

    @staticmethod
    def now(actor: str) -> "AuditStamp":
        now = datetime.now(timezone.utc)
        return AuditStamp(actor, now, actor, now)

    def touch(self, actor: str) -> "AuditStamp":
        now = datetime.now(timezone.utc)
        return replace(self, updated_at=now, updated_by=actor)
