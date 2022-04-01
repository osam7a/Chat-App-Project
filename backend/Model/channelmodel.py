from typing import List, Optional
from pydantic import BaseModel
from usermodel import User
from messagemodel import Message

class Channel(BaseModel):
    ID: int
    chName: str
    chPassword: str
    messages: List[Message]
    users: List[User]
    meta: Optional[dict]
