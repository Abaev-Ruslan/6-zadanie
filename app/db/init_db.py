from app.db.db import SessionLocal, engine, Base
from app.db import crud

def init_database():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Создаем категории
        categories = ["Фантастика", "Детектив"]
        category_objects = {}
        
        for cat_title in categories:
            existing = crud.get_category_by_title(db, cat_title)
            if not existing:
                category = crud.create_category(db, cat_title)
                category_objects[cat_title] = category
                print(f"✅ Создана категория: {cat_title}")
            else:
                category_objects[cat_title] = existing
                print(f"⚠️ Категория уже существует: {cat_title}")
        
        # Книги для категории "Фантастика"
        fantasy_books = [
            {"title": "Дюна", "description": "Эпическая научно-фантастическая сага", "price": 890.00},
            {"title": "1984", "description": "Роман-антиутопия", "price": 650.00},
            {"title": "Автостопом по Галактике", "description": "Юмористическая фантастика", "price": 520.00},
        ]
        
        # Книги для категории "Детектив"
        detective_books = [
            {"title": "Убийство в Восточном экспрессе", "description": "Классический детектив Агаты Кристи", "price": 720.00},
            {"title": "Шерлок Холмс", "description": "Сборник рассказов о великом сыщике", "price": 890.00},
        ]
        
        # Добавляем книги для Фантастики
        fantasy_cat = category_objects["Фантастика"]
        for book_data in fantasy_books:
            existing_books = crud.get_books_by_category(db, fantasy_cat.id)
            if not any(b.title == book_data["title"] for b in existing_books):
                crud.create_book(
                    db,
                    title=book_data["title"],
                    description=book_data["description"],
                    price=book_data["price"],
                    category_id=fantasy_cat.id
                )
                print(f"📚 Добавлена книга: {book_data['title']} в категорию 'Фантастика'")
            else:
                print(f"📖 Книга уже существует: {book_data['title']}")
        
        # Добавляем книги для Детектива
        detective_cat = category_objects["Детектив"]
        for book_data in detective_books:
            existing_books = crud.get_books_by_category(db, detective_cat.id)
            if not any(b.title == book_data["title"] for b in existing_books):
                crud.create_book(
                    db,
                    title=book_data["title"],
                    description=book_data["description"],
                    price=book_data["price"],
                    category_id=detective_cat.id
                )
                print(f"📚 Добавлена книга: {book_data['title']} в категорию 'Детектив'")
            else:
                print(f"📖 Книга уже существует: {book_data['title']}")
        
        print("\n🎉 База данных успешно инициализирована!")
        
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
