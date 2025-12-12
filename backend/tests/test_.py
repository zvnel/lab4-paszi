import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.user import User
from app.core.config import settings

# подключение к бд
engine = create_engine(settings.DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# создание сессии
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# генерация логина
def _unique_login(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def test_register_success():
    # Успешная регистрация нового пользователя
    login = _unique_login("pytest_user_ok")

    r = client.post("/api/register", json={"login": login, "password": "Strong!1Pass"})
    assert r.status_code == 201

    # проверяем, что пользователь реально сохранён в БД
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter_by(login=login).first()
        assert user is not None
    finally:
        db.close()


def test_register_duplicate_login():
    # повторный логин
    login = _unique_login("pytest_user_dup")

    r1 = client.post("/api/register", json={"login": login, "password": "Strong!1Pass"})
    assert r1.status_code == 201

    r2 = client.post("/api/register", json={"login": login, "password": "Another!1Pass"})
    assert r2.status_code == 409


def test_weak_password():
    # слабый пароль
    login = _unique_login("pytest_user_weak")

    r = client.post("/api/register", json={"login": login, "password": "abc"})
    assert r.status_code == 422
