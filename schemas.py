from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    name: str
    user_name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class UserInDB(User):
    hashed_password: str

class TimeLogBase(BaseModel):
    action: str  # 'check-in' ou 'check-out'

class TimeLogCreate(TimeLogBase):
    pass

class TimeLog(TimeLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True