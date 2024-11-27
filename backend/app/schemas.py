from pydantic import BaseModel
import uuid

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class UserInDB(UserBase):
    id: uuid.UUID
    password: str

    class Config:
        from_attributes = True
