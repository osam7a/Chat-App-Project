from typing import List, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str
    username: str
    admin: bool = False
    meta: Optional[dict]

class Message(BaseModel):
    id: Optional[str] = Field(alias='_id')
    created_at: int
    author: User
    content: str

class Channel(BaseModel):
    id: Optional[str] = Field(alias='_id')
    created_at: int
    name: str
    hash: Optional[str]
    messages: List[Message]
    users: List[User]
    meta: Optional[dict]