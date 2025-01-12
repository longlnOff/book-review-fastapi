from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import (
    select,
    desc
)
from datetime import datetime


from src.books.schemas import (
    BookCreateModel,
    BookUpdateModel
)
from src.books.models import Book


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_a_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_a_book(self, book_data: BookCreateModel, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(
            **book_data_dict
        )
        new_book.published_date = datetime.strptime(book_data_dict["published_date"], "%Y-%m-%d")
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_a_book(self, book_uid: str, book_data: BookUpdateModel, session: AsyncSession):
        book_to_update = await self.get_a_book(book_uid, session)
        if not book_to_update:
            return None

        book_data_dict = book_data.model_dump()

        for key, value in book_data_dict.items():
            setattr(book_to_update, key, value)

        await session.commit()
        return book_to_update
    
    async def delete_a_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_a_book(book_uid, session)
        if book_to_delete is None:
            return None
        await session.delete(book_to_delete)
        await session.commit()
        return book_to_delete
