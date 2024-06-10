from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.settings import get_settings

settings = get_settings()

engine = create_engine(
    url=settings.DATABASE_URI, pool_pre_ping=True, pool_recycle=3600, pool_size=20, max_overflow=0
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
