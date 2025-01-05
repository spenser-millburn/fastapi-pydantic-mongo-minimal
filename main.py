from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
import uvicorn

from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    description: str
    published_year: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adams",
                "description": "A humorous science fiction novel.",
                "published_year": 1979
            }
        }

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["my_book_database"]
collection = db["books"]

@app.post("/books", response_model=Book)
async def create_book(book: Book):
  book_dict = book.dict()
  collection.insert_one(book_dict)
  return book

@app.get("/books")
async def get_books():
  books = []
  for book in collection.find():
    books.append(Book(**book))
  return books

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: str):
  book = collection.find_one({"_id": ObjectId(book_id)})
  if book:
    return Book(**book)
  else:
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book: Book):
  book_dict = book.dict()
  collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
  return book

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
