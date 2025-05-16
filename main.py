import uvicorn
import datetime
from fastapi import FastAPI, HTTPException
from uuid import uuid4
from models import *
from database import *
from auth_utils import create_access_token, verify_token
from fastapi import Header, Depends

app = FastAPI()
mongo_db = MongoConnect()

@app.get("/user_info")
async def get_user(id: str):
    user = mongo_db.users_collection.find_one(
        {"user_id": id},
        {"_id": 0, "user_id": 1, "first_name": 1, "last_name": 1, "email": 1, "phone": 1, "gender": 1, "joined_at": 1}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"msg": "Success", "data": user}

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
    print("Login attempt with:", payload.email, payload.password)

    user = mongo_db.users_collection.find_one({
        "email": payload.email
    })

    print("User found:", user)

    if user and user["password"] == payload.password:
        token = create_access_token({"user_id": user["user_id"]})
        return {"msg": "Login successful", "access_token": token}
    else:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

@app.post("/insert_notes")
def notes_insert(note: NoteInsert, token: str = Header(...)):
    user_id = verify_token(token)  # verifies token and extracts user_id

    note_id = str(uuid4())
    mongo_db.notes_collection.insert_one({
        "note_id": note_id,
        "user_id": user_id,  # associate note with logged-in user
        "title": note.title,
        "body": note.content,
        "created_at": note.created_at
    })
    return {'msg': 'notes created successfully', 'note_id': note_id, 'title': note.title}

@app.put("/update_notes")
def notes_update(update: NoteUpdate, token: str = Header(...)):
    user_id = verify_token(token)  # verify token

    # You may want to check if the note belongs to user_id here (optional for extra security)
    mongo_db.notes_collection.update_one(
        {'note_id': update.note_id}, {"$set": {"body": update.content}}
    )
    return {'msg': 'updated successfully', 'title': update.title, 'body': update.content}

@app.get("/notes")
def get_notes(token: str = Header(...)):
    user_id = verify_token(token)
    print("User ID from token:", user_id)
    notes = list(mongo_db.notes_collection.find({"user_id": user_id}, {"_id": 0}))
    print(f"Found {len(notes)} notes for user_id {user_id}")
    return {"msg": "Success", "data": notes}

if __name__ == "__main__":
    uvicorn.run(app)