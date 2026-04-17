from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(f"sqlite+pysqlite:///{settings.db_path}", future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
