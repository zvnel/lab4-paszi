from pydantic import BaseModel, Field, validator
import re

# схема входных данных для регистрации
class UserCreate(BaseModel):
    # логин пользователя
    login: str = Field(..., min_length=3, max_length=32)
    # пароль
    password: str = Field(..., min_length=8)
    # проверка допустимых символов логина
    @validator("login")
    def validate_login(cls, v: str) -> str:
        pattern = r"^[A-Za-z0-9._-]{3,32}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Логин может содержать только латинские буквы, цифры и символы"
            )
        return v
    # проверка сложности пароля
    @validator("password")
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен быть не короче 8 символов")
        if not re.search(r"[a-z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"[0-9]", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Пароль должен содержать хотя бы один спецсимвол")
        return v

# схема ответа
class UserResponse(BaseModel):
    message: str
