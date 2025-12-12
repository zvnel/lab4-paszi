from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base
# модель пользователя
class User(Base):
    # имя таблицы в базе данных
    __tablename__ = "users"
    # первичный ключ
    id = Column(Integer, primary_key=True, index=True)
    # логин пользователя (уникальный)
    login = Column(String(32), unique=True, nullable=False, index=True)
    # хеш пароля (Argon2)
    password_hash = Column(String, nullable=False)
    # время создания пользователя
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
