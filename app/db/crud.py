from sqlalchemy.orm import Session
from app.db import models

# ---------- CRUD для Category ----------
def create_category(db: Session, title: str):
    category = models.Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_category_by_title(db: Session, title: str):
    return db.query(models.Category).filter(models.Category.title == title).first()

def get_all_categories(db: Session):
    return db.query(models.Category).all()

def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category

# ---------- Дополнительные функции для API ----------
def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def update_category(db: Session, category_id: int, **kwargs):
    """Обновляет категорию, принимает любые поля"""
    category = get_category_by_id(db, category_id)
    if not category:
        return None
    for key, value in kwargs.items():
        if hasattr(category, key) and value is not None:
            setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

# ---------- CRUD для Book ----------
def create_book(db: Session, title: str, description: str, price: float, category_id: int, url: str = ""):
    book = models.Book(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        url=url
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_books_by_category(db: Session, category_id: int):
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def get_all_books(db: Session):
    return db.query(models.Book).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_book(db: Session, book_id: int, **kwargs):
    """Универсальный метод обновления книги. Принимает любые поля"""
    book = get_book_by_id(db, book_id)
    if not book:
        return None
    for key, value in kwargs.items():
        if hasattr(book, key) and value is not None:
            setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
    return book
