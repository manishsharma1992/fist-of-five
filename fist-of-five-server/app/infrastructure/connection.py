from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.config.settings import settings

engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    connect_args={
        "options": f"-c search_path={settings.database_schema},public"
    }
)

# Session factory (like Spring's EntityManager)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI (like Spring's @Autowired)
def get_db():
    """
    Database session dependency
    Usage in FastAPI: def my_endpoint(db: Session = Depends(get_db))
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()