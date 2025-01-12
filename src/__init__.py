from fastapi import (
    FastAPI
)
import src.books.routes as book_routes


version = "v1"

app = FastAPI(
    title="Book Review API",
    description="REST API for book reviews webservice",
    version=version
)


app.include_router(
    book_routes.router,
    prefix="/api{version}/books",
    tags=["books"]
)