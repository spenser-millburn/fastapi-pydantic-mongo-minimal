from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
from pydantic import BaseModel
from typing import List, Dict

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

class User(BaseModel):
    email: str
    name: str
    authProvider: Dict

class Dataset(BaseModel):
    name: str
    description: str
    source: str
    data: str

class Session(BaseModel):
    userId: str
    name: str
    createdDate: str

class Graph(BaseModel):
    sessionId: str
    name: str
    type: str

class Data(BaseModel):
    graphId: str
    datasetId: str
    filters: Dict

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]
books_collection = db["books"]
users_collection = db["users"]
datasets_collection = db["datasets"]
sessions_collection = db["sessions"]
graphs_collection = db["graphs"]
data_collection = db["data"]

@app.post("/books", response_model=Book, tags=["Books"])
async def create_book(book: Book):
    book_dict = book.dict()
    books_collection.insert_one(book_dict)
    return book

@app.get("/books", tags=["Books"])
async def get_books():
    books = []
    for book in books_collection.find():
        books.append(Book(**book))
    return books

@app.get("/books/{book_id}", response_model=Book, tags=["Books"])
async def get_book(book_id: str):
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        return Book(**book)
    else:
        raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book, tags=["Books"])
async def update_book(book_id: str, book: Book):
    book_dict = book.dict()
    books_collection.update_one({"_id": ObjectId(book_id)}, {"$set": book_dict})
    return book

@app.post("/users", response_model=User, tags=["Users"])
async def create_user(user: User):
    user_dict = user.dict()
    users_collection.insert_one(user_dict)
    return user

@app.get("/users", tags=["Users"])
async def get_users():
    users = []
    for user in users_collection.find():
        users.append(User(**user))
    return users

@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(**user)
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/datasets", response_model=Dataset, tags=["Datasets"])
async def create_dataset(dataset: Dataset):
    dataset_dict = dataset.dict()
    datasets_collection.insert_one(dataset_dict)
    return dataset

@app.get("/datasets", tags=["Datasets"])
async def get_datasets():
    datasets = []
    for dataset in datasets_collection.find():
        datasets.append(Dataset(**dataset))
    return datasets

@app.get("/datasets/{dataset_id}", response_model=Dataset, tags=["Datasets"])
async def get_dataset(dataset_id: str):
    dataset = datasets_collection.find_one({"_id": ObjectId(dataset_id)})
    if dataset:
        return Dataset(**dataset)
    else:
        raise HTTPException(status_code=404, detail="Dataset not found")

@app.post("/sessions", response_model=Session, tags=["Sessions"])
async def create_session(session: Session):
    session_dict = session.dict()
    sessions_collection.insert_one(session_dict)
    return session

@app.get("/sessions", tags=["Sessions"])
async def get_sessions():
    sessions = []
    for session in sessions_collection.find():
        sessions.append(Session(**session))
    return sessions

@app.get("/sessions/{session_id}", response_model=Session, tags=["Sessions"])
async def get_session(session_id: str):
    session = sessions_collection.find_one({"_id": ObjectId(session_id)})
    if session:
        return Session(**session)
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.post("/graphs", response_model=Graph, tags=["Graphs"])
async def create_graph(graph: Graph):
    graph_dict = graph.dict()
    graphs_collection.insert_one(graph_dict)
    return graph

@app.get("/graphs", tags=["Graphs"])
async def get_graphs():
    graphs = []
    for graph in graphs_collection.find():
        graphs.append(Graph(**graph))
    return graphs

@app.get("/graphs/{graph_id}", response_model=Graph, tags=["Graphs"])
async def get_graph(graph_id: str):
    graph = graphs_collection.find_one({"_id": ObjectId(graph_id)})
    if graph:
        return Graph(**graph)
    else:
        raise HTTPException(status_code=404, detail="Graph not found")

@app.post("/data", response_model=Data, tags=["Data"])
async def create_data(data: Data):
    data_dict = data.dict()
    data_collection.insert_one(data_dict)
    return data

@app.get("/data", tags=["Data"])
async def get_data():
    data_list = []
    for data in data_collection.find():
        data_list.append(Data(**data))
    return data_list

@app.get("/data/{data_id}", response_model=Data, tags=["Data"])
async def get_data_item(data_id: str):
    data = data_collection.find_one({"_id": ObjectId(data_id)})
    if data:
        return Data(**data)
    else:
        raise HTTPException(status_code=404, detail="Data not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
