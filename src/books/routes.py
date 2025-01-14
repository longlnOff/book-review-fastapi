from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID

from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.db.main import get_session
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()

@router.get("/", response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    user_details=Depends(access_token_bearer),
):
    books = await book_service.get_all_books(session)
    return books


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)):
    new_book = await book_service.create_a_book(book_data, session)
    return new_book


@router.get("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_a_book(book_uid: UUID, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_a_book(book_uid=book_uid, 
                                   session=session)
    if book is not None:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.patch("/{book_uid}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_a_book(book_uid: UUID, book_update_data: BookUpdateModel, session: AsyncSession = Depends(get_session)):
    updated_book = await book_service.update_a_book(book_uid=book_uid, 
                                              book_data=book_update_data, 
                                              session=session)
    if updated_book is not None:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@router.delete("/{book_uid}", response_model={}, status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_uid: UUID, session: AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_a_book(book_uid=book_uid, 
                                              session=session)
    if deleted_book is not None:
        return {}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
