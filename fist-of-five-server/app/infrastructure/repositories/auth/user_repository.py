from typing import Optional

from app.domain.auth import User, Role
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_email(self, email: str) -> Optional[User]:
        """
        Find user by email
        :param email:
        :return:
        """
        return self.db.query(User).filter_by(email=email).first()

    def find_by_uid(self, uid: str) -> Optional[User]:
        """
        Find user by uid
        :param uid:
        :return:
        """
        return self.db.query(User).filter_by(uid=uid).first()

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def exists_by_email(self, email: str) -> bool:
        """
        Check if email already exists
        :param email:
        :return:
        """
        return self.find_by_email(email) is not None

    def exists_by_uid(self, uid: str) -> bool:
        """
        Check if uid already exists
        :param uid:
        :return:
        """
        return self.find_by_uid(uid) is not None