from pydantic import BaseModel, Field, field_validator
from typing import Optional


# ---------- Схемы для Category ----------
class CategoryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Название категории не может быть пустым")
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Название категории не может быть пустым")
        return v


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Схемы для Book ----------
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = Field(None, max_length=2000)
    price: float = Field(..., gt=0, description="Цена должна быть больше 0")
    url: Optional[str] = ""
    category_id: int = Field(..., gt=0)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Название книги не может быть пустым")
        return v

    @field_validator("url")
    @classmethod
    def url_valid(cls, v: Optional[str]) -> Optional[str]:
        if v and not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("url должен начинаться с http:// или https://")
        return v


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=300)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[float] = Field(None, gt=0)
    url: Optional[str] = None
    category_id: Optional[int] = Field(None, gt=0)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Название книги не может быть пустым")
        return v

    @field_validator("url")
    @classmethod
    def url_valid(cls, v: Optional[str]) -> Optional[str]:
        if v and not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError("url должен начинаться с http:// или https://")
        return v


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
