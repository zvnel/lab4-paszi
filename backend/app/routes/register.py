from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserCreate, UserResponse
from ..core.security import hash_password
# роутер для регистрации
router = APIRouter(prefix="/api", tags=["auth"])
# события регистрации
logger = logging.getLogger("register")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # проверяем, что логин уникальный
    existing = db.query(User).filter(User.login == payload.login).first()
    if existing:
        logger.info("Попытка регистрации уже существующего логина: %s", payload.login)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким логином уже существует",
        )

    # хэшируем пароль
    password_hash = hash_password(payload.password)
    # создаём ORM-объект пользователя
    user = User(
        login=payload.login,
        password_hash=password_hash,
    )
    # сохраняем в БД
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("Успешная регистрация пользователя: %s", user.login)
    # возвращаем ответ клиенту
    return UserResponse(message="user создан")
