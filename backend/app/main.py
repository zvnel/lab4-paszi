import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db
from .routes.register import router as register_router

# логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
# создание FastAPI-приложения
app = FastAPI(title="Lab4 MVP")

# CORS (для фронтенда на Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# подключаем роутер регистрации
app.include_router(register_router)

# проверка
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    # простая проверка подключения к БД
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
