from pydantic import BaseModel
from typing import List
from messagemodel import Message
from usermodel import User

class User(BaseModel):
    ID: int
    username: str
    password: str
    direct_messages: dict[User, List[Message]]
    meta: dict