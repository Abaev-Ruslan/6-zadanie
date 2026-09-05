from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse])
def get_books(
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    db: Session = Depends(get_db)
):
    """Получить список книг. Можно фильтровать по category_id"""
    if category_id:
        category = crud.get_categories(db, category_id=category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    return crud.get_books(db, category_id=category_id)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    book = crud.get_books(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    category = crud.get_categories(db, category_id=book.category_id)
    if not category:
        raise HTTPException(status_code=400, detail="Category not found")
    return crud.create_book(
        db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url or ""
    )

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу"""
    # Проверяем, существует ли книга
    existing_book = crud.get_books(db, book_id=book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Проверяем категорию, если она передана
    if book.category_id is not None:
        category = crud.get_categories(db, category_id=book.category_id)
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")

    # Вызываем универсальный метод обновления из CRUD
    updated_book = crud.update_book(
        db,
        book_id,
        title=book.title,
        description=book.description,
        price=book.price,
        url=book.url,
        category_id=book.category_id
    )

    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    book = crud.get_books(db, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book_id)
    return None
