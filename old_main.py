from app.db.db import SessionLocal
from app.db import crud

def display_data():
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("📚 КАТАЛОГ КНИГ".center(60))
        print("="*60)
        
        categories = crud.get_all_categories(db)
        
        for category in categories:
            print(f"\n📖 Категория: {category.title}")
            print("-" * 40)
            
            books = crud.get_books_by_category(db, category.id)
            
            if not books:
                print("  Нет книг в этой категории")
            else:
                for i, book in enumerate(books, 1):
                    print(f"  {i}. {book.title}")
                    print(f"     Описание: {book.description}")
                    print(f"     Цена: {book.price:.2f} ₽")
                    print(f"     Ссылка: {book.url if book.url else '—'}")
                    print()
        
        print("\n" + "="*60)
        print(f"📊 Всего категорий: {len(categories)}")
        
        all_books = crud.get_all_books(db)
        print(f"📊 Всего книг: {len(all_books)}")
        print("="*60 + "\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    display_data()
