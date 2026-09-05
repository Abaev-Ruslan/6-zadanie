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


def get_categories(db: Session, category_id: int = None):
    """
    Универсальный метод получения категорий.
    - category_id указан -> вернуть одну категорию (или None)
    - category_id не указан -> вернуть список всех категорий
    """
    query = db.query(models.Category)
    if category_id is not None:
        return query.filter(models.Category.id == category_id).first()
    return query.all()


def update_category(db: Session, category_id: int, **kwargs):
    """Обновляет категорию, принимает любые поля"""
    category = get_categories(db, category_id=category_id)
    if not category:
        return None
    for key, value in kwargs.items():
        if hasattr(category, key) and value is not None:
            setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = get_categories(db, category_id=category_id)
    if category:
        db.delete(category)
        db.commit()
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


def get_books(db: Session, book_id: int = None, category_id: int = None):
    """
    Универсальный метод получения книг.
    - book_id указан -> вернуть одну книгу (или None), category_id при этом игнорируется
    - category_id указан (без book_id) -> вернуть список книг этой категории
    - ничего не указано -> вернуть список всех книг
    """
    if book_id is not None:
        return db.query(models.Book).filter(models.Book.id == book_id).first()

    query = db.query(models.Book)
    if category_id is not None:
        query = query.filter(models.Book.category_id == category_id)
    return query.all()


def update_book(db: Session, book_id: int, **kwargs):
    """Универсальный метод обновления книги. Принимает любые поля"""
    book = get_books(db, book_id=book_id)
    if not book:
        return None
    for key, value in kwargs.items():
        if hasattr(book, key) and value is not None:
            setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = get_books(db, book_id=book_id)
    if book:
        db.delete(book)
        db.commit()
    return book
