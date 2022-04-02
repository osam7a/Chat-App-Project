from pydantic import BaseModel
from typing import List, Dict, Optional
from messagemodel import Message
from usermodel import User

class User(BaseModel):
    ID: int
    username: str
    password: str
    direct_messages: List[dict]
    meta: Optional[dict]