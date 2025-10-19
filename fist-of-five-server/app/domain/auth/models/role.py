from sqlalchemy import Column, Integer, String

from app.infrastructure.database.base import Base

SCHEMA = "agile_scrum"

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {'schema': SCHEMA}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Role(name='{self.name}')>"