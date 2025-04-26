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

class UserLogin(BaseModel):
    email: str
    password: str

class NoteInsert(BaseModel):
    title: str
    content: str
    user_id: str

class NoteUpdate(NoteInsert):
    note_id: str
