from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .core.config import settings

# движок к  БД paszi
engine = create_engine(
    settings.DATABASE_URL,
    future=True,
    echo=True,
)
# создание сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
# базовый класс
Base = declarative_base()

# dependency для FastAPI для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
