import uvicorn
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
    return {'Message': "Successfull", "Data": users['user_id']}

@app.post("/register")
def register(payload: UserRegister):
    if mongo_db.users_collection.find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Username exists")
    user_id = str(uuid4())
    mongo_db.users_collection.insert_one({
        "user_id": user_id,
        "first_name": payload.first_name,
        "last_name" : payload.last_name,
        "email": payload.email,
        "phone": payload.phone,
        "gender": payload.gender,
        "password": payload.password
    })
    return {"msg": f"Registered {payload.first_name}", "email": payload.email}

@app.post("/login")
def login(payload: UserLogin):
    if mongo_db.users_collection.find_one({"email": payload.email,
                                  "password": payload.password}, {"email", 'password'}):
        return {'msg': 'login successful', "user_email": payload.email}
    else:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

if __name__ == "__main__":
    uvicorn.run(app)