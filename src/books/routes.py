from fastapi import (
    APIRouter,
    status,
    HTTPException
)

from src.books.book_data import books
from src.books.schemas import Book, BookUpdateModel 

router = APIRouter()

@router.get("/", response_model=list[Book])
async def get_all_books():
    return books

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_a_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Book not found")

@router.patch("/{book_id}")
async def update_a_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['publisher'] = book_update_data.publisher
            book['published_date'] = book_update_data.published_date
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Book not found")

@router.delete("/{book_id}")
async def delete_a_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Book not found")

