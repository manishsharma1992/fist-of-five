from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

from app.infrastructure.config.settings import settings

# Create metadata with schema
metadata = MetaData(schema=settings.database_schema)


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models
    Similar to JPA's @Entity base
    """
    metadata = metadata