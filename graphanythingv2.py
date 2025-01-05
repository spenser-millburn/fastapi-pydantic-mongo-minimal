from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
from pydantic import BaseModel
from typing import Dict, Type

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["my_database"]

def create_crud_endpoints(model: Type[BaseModel], collection_name: str):
    collection = db[collection_name]

    @app.post(f"/{collection_name}", response_model=model, tags=[collection_name.capitalize()])
    async def create_item(item: model):
        item_dict = item.dict()
        collection.insert_one(item_dict)
        return item

    @app.get(f"/{collection_name}", tags=[collection_name.capitalize()])
    async def get_items():
        items = []
        for item in collection.find():
            items.append(model(**item))
        return items

    @app.get(f"/{collection_name}/{{item_id}}", response_model=model, tags=[collection_name.capitalize()])
    async def get_item(item_id: str):
        item = collection.find_one({"_id": ObjectId(item_id)})
        if item:
            return model(**item)
        else:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

    @app.put(f"/{collection_name}/{{item_id}}", response_model=model, tags=[collection_name.capitalize()])
    async def update_item(item_id: str, item: model):
        item_dict = item.dict()
        collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_dict})
        return item

    @app.delete(f"/{collection_name}/{{item_id}}", tags=[collection_name.capitalize()])
    async def delete_item(item_id: str):
        result = collection.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 1:
            return {"message": f"{model.__name__} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

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

create_crud_endpoints(Book, "books")
create_crud_endpoints(User, "users")
create_crud_endpoints(Dataset, "datasets")
create_crud_endpoints(Session, "sessions")
create_crud_endpoints(Graph, "graphs")
create_crud_endpoints(Data, "data")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
