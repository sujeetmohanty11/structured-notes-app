import uvicorn
import datetime
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from models import *
from database import *

app = FastAPI()
mongo_db = MongoConnect()


@app.get("/user_info")
async def get_user(id: str):
    users = list(mongo_db.users_collection.find({"user_id": id}, {'user_id', 'password', 'joined_on', 'gender'}))[0]
    print(users, type(users['user_id']))
    return {'msg': "Successful", "data": users['user_id']}


@app.post("/register")
def register(payload: UserRegister):
    if mongo_db.users_collection.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Username exists")
    user_id = str(uuid4())
    mongo_db.users_collection.insert_one({
        "user_id": user_id,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "email": payload.email,
        "phone": payload.phone,
        "gender": payload.gender,
        "password": payload.password,
        "joined_at": payload.joined_at
    })
    return {"msg": f"Registered {payload.first_name}", "email": payload.email}


@app.post("/login")
def login(payload: UserLogin):
    if mongo_db.users_collection.find_one({"email": payload.email,
                                           "password": payload.password}, {"email", 'password'}):
        return {'msg': 'login successful', "user_email": payload.email}
    else:
        raise HTTPException(status_code=400, detail="Incorrect email or password")


@app.post("/insert_notes")
def notes_insert(note: NoteInsert):
    note_id = str(uuid4())
    mongo_db.notes_collection.insert_one({
        "note_id": note_id,
        "user_id": note.user_id,
        "title": note.title,
        "body": note.content,
        "created_at": note.created_at
    })
    return {'msg': 'notes created successfully', 'note_id': {note_id}, 'title': {note.title}}


@app.put("/update_notes")
def notes_update(update: NoteUpdate):
    mongo_db.notes_collection.update_one(
        {'note_id': update.note_id}, {"$set": {"body": update.content}}
    )
    return {'msg': 'updated successfully', 'title': update.title, 'body': update.content}


if __name__ == "__main__":
    uvicorn.run(app)
