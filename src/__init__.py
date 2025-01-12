from fastapi import (
    FastAPI
)
import src.books.routes as book_routes
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting ...")
    print("initializing database ...")
    await init_db()
    yield
    print("server is shutting down ...")

version = "v1"

app = FastAPI(
    title="Book Review API",
    description="REST API for book reviews webservice",
    version=version,
    lifespan=lifespan
)


app.include_router(
    book_routes.router,
    prefix="/api{version}/books",
    tags=["books"]
)
