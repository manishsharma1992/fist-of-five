from src.domain.auth.commands.commands import UpsertUserCmd
from src.domain.auth.ports.ports import UserFactory
from src.domain.auth.repository.role_repository import RoleRepository
from src.domain.auth.repository.user_repository import UserRepository
from src.domain.auth.aggregate.entities import User
from src.utils.password_hasher import PasswordService


class AuthenticationDomainService:
    def __init__(
            self,
            user_factory: UserFactory,
            user_repository: UserRepository,
            role_repository: RoleRepository,
            password_service: PasswordService
    ):
        self._userFactory = user_factory
        self._userRepository = user_repository
        self._roleRepository = role_repository
        self._passwordService = password_service

    def save(self, cmd: UpsertUserCmd) -> User:
        if cmd.id is None:
            return self._create(cmd)
        else:
            return self._update(cmd)

        # ---------- private ----------

    def _create(self, cmd: UpsertUserCmd) -> User:
        # Validate required fields for creation
        if not all([cmd.uid, cmd.first_name, cmd.last_name, cmd.username, cmd.password_plain]):
            raise ValueError(
                "Missing required fields for create (uid, first_name, last_name, username, password_plain)")

        hashed = self._passwordService.hash(cmd.password_plain)
        role_ids = frozenset(cmd.role_ids or frozenset())

        # delegate to the factory that actually inserts + returns domain User
        return self._userFactory.create_user(
            uid=cmd.uid,
            first_name=cmd.first_name,
            last_name=cmd.last_name,
            username=cmd.username,
            password_hash=hashed,
            role_ids=role_ids,
            actor=cmd.actor,
        )

    def _update(self, cmd: UpsertUserCmd) -> User:
        user = self._userRepository.by_id(cmd.id)
        if not user:
            raise ValueError(f"User {cmd.id} not found")

        u = user
        # apply partial changes via withers; pass actor for audit.touch
        if cmd.first_name is not None:
            u = u.with_first_name(first_name=cmd.first_name, actor=cmd.actor)
        if cmd.last_name is not None:
            u = u.with_last_name(last_name=cmd.last_name, actor=cmd.actor)
        if cmd.username is not None:
            u = u.with_username(username=cmd.username, actor=cmd.actor)
        if cmd.uid is not None:
            u = u.with_uid(uid=cmd.uid, actor=cmd.actor)

        if cmd.password_plain is not None:
            new_hash = self._passwordService.hash(cmd.password_plain)
            u = u.with_password_hash(password_hash=new_hash, actor=cmd.actor)

        if cmd.role_ids is not None:
            roles = self._roleRepository.by_ids(frozenset(cmd.role_ids))
            u = u.with_roles(roles=roles, actor=cmd.actor)

        return self._userRepository.save(u)
