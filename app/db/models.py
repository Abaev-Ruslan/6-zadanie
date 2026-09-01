from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    
    books = relationship("Book", back_populates="category")
    
    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.title}')>"

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    url = Column(String, nullable=True, default="")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    category = relationship("Category", back_populates="books")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', price={self.price})>"
