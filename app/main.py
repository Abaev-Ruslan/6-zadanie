from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import books, categories
from app.db.db import engine, Base

# Создаём таблицы при запуске
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book API",
    description="API для управления книгами и категориями",
    version="1.0.0"
)

# Настройка CORS (для тестирования из браузера)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(books.router)
app.include_router(categories.router)

@app.get("/health")
def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok", "message": "Сервис работает!"}

@app.get("/")
def root():
    return {"message": "Добро пожаловать в Book API!", "docs": "/docs"}
