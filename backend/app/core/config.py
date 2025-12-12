import os
from dotenv import load_dotenv
from pydantic import BaseModel

# загружаем переменные окружения из файла .env
# файл ищется вверх по дереву каталогов от текущей рабочей директории
load_dotenv()

class Settings(BaseModel):
    # строка подключения к PostgreSQL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    # алгоритм хеширования паролей
    HASH_SCHEME: str = os.getenv("HASH_SCHEME", "argon2")
    # секретный ключ приложения
    SECRET_KEY: str = os.getenv("SECRET_KEY", "devsecret")
    # окружение приложения
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    # параметры алгоритма Argon2
    ARGON2_TIME_COST: int = int(os.getenv("ARGON2_TIME_COST", "2"))
    ARGON2_MEMORY_COST: int = int(os.getenv("ARGON2_MEMORY_COST", "102400"))
    ARGON2_PARALLELISM: int = int(os.getenv("ARGON2_PARALLELISM", "8"))
# глобальный объект конфигурации
settings = Settings()
