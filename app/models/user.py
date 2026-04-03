import uuid
from datetime import datetime
from typing import Optional, Annotated 
from pydantic import Field
from beanie import Document, Indexed

class User(Document):
  
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
 
    email: Annotated[str, Indexed(unique=True)]
    
    hashed_password: Optional[str] = None
    salt: Optional[str] = None

    yandex_id: Annotated[Optional[str], Indexed(unique=True)] = None
    vk_id: Annotated[Optional[str], Indexed(unique=True)] = None

    is_active: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
 
    deleted_at: Optional[datetime] = None

    class Settings:
        name = "users"

    def __repr__(self):
        return f"<User(email={self.email}, active={self.is_active})>"