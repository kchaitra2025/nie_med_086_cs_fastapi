from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel

from pymongo import MongoClient
from bson import ObjectId

# app 
app = FastAPI()

# db config
URL = "mongodb://127.0.0.1:27017"
client = MongoClient(URL)
db = client["service_ticket_db"]
ticket_collection = db["tickets"]

# schema pydantic
class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str
    
class TicketResponse(BaseModel):
    id: str
    
# helper
def ticket_helper(ticket_doc):
    return {
        "id": str(ticket_doc["_id"]),
        "title": str(ticket_doc["title"]),
        "description": str(ticket_doc["description"]),
        "status": str(ticket_doc["status"]),
}

# apis - CRUD - create,read all, read by id,update, delete
@app.post("/tickets", status_code=201, response_model=TicketResponse)
def ticket_create(payload: TicketCreate):
    ticket_dict = payload.model_dump()