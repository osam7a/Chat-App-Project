from pydantic import BaseModel, Field
from typing import List, Optional

class Channel(BaseModel):
    id: str = Field(alias='_id')
    name: str
    public: bool
    joined_at: int
    meta: Optional[dict]

class User(BaseModel):
    id: Optional[str] = Field(alias='_id')
    username: str
    hash: str
    channels: List[Channel]
    meta: Optional[dict]