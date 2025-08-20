import os
from dataclasses import dataclass
from typing import Optional

from argon2 import PasswordHasher
from argon2.low_level import Type


@dataclass(frozen=True)
class PasswordServiceConfig:
    # Argon2id parameters (tune per your infra)
    time_cost: int = 3
    memory_cost_kib: int = 64 * 1024  # 64 MB
    parallelism: int = 2
    hash_len: int = 32
    pepper: str = os.getenv("PASSWORD_PEPPER", "")  # optional, keep in env/KMS


class PasswordService:
    """
    One-way password hashing/verification using Argon2id.
    - Stores only the encoded Argon2 string (contains salt + params).
    - Optional pepper for defense-in-depth (prepend to plaintext).
    """

    def __init__(self, config: Optional[PasswordServiceConfig] = None):
        cfg = config or PasswordServiceConfig()
        object.__setattr__(self, "_pepper", cfg.pepper)
        object.__setattr__(
            self,
            "_ph",
            PasswordHasher(
                time_cost=cfg.time_cost,
                memory_cost=cfg.memory_cost_kib,
                parallelism=cfg.parallelism,
                hash_len=cfg.hash_len,
                type=Type.ID,  # Argon2id
            ),
        )

    # ---------- public API ----------

    def hash(self, plain: str) -> str:
        """Return encoded Argon2 hash string (includes salt and params)."""
        return self._ph.hash(self._pepper + plain)

    def verify(self, hashed: str, plain: str) -> bool:
        """Verify plaintext against stored hash."""
        try:
            return self._ph.verify(hashed, self._pepper + plain)
        except Exception:
            return False

    def needs_rehash(self, hashed: str) -> bool:
        """Check if stored hash should be upgraded to stronger params."""
        return self._ph.check_needs_rehash(hashed)

    def verify_and_upgrade(self, hashed: str, plain: str) -> tuple[bool, Optional[str]]:
        """
        Verify and, if params are outdated, return a new upgraded hash.
        Usage:
            ok, new_hash = svc.verify_and_upgrade(user.password_hash, input_pwd)
            if ok and new_hash:  # persist new_hash
        """
        if not self.verify(hashed, plain):
            return False, None
        if self.needs_rehash(hashed):
            return True, self.hash(plain)
        return True, None
