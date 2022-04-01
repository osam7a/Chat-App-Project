from typing import List
from pydantic import BaseModel
from typing import List
from usermodel import User
from messagemodel import Message

class Channel(BaseModel):
    ID: int
    chName: str
    chPassword: str
    messages: List[Message]
    users: List[User]
    meta: dict
