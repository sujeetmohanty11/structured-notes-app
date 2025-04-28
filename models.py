from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    gender: str
    password: str
    joined_at: Optional[datetime] = datetime.utcnow()

class UserLogin(BaseModel):
    email: str
    password: str

class NoteInsert(BaseModel):
    title: str
    content: str
    user_id: str
    created_at: Optional[datetime] = datetime.utcnow()

class NoteUpdate(NoteInsert):
    note_id: str
    updated_at: Optional[datetime] = datetime.utcnow()
