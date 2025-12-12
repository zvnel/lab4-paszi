from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(
    schemes=["argon2"], # алгоритм хеширования
    deprecated="auto", # поддержка миграций
    argon2__time_cost=settings.ARGON2_TIME_COST, # число итераций
    argon2__memory_cost=settings.ARGON2_MEMORY_COST, # объём памяти
    argon2__parallelism=settings.ARGON2_PARALLELISM, # число потоков
)


def hash_password(password: str) -> str:
    # хэш
    return pwd_context.hash(password)
