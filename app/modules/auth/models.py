from beanie import Document
from pydantic import BaseModel, EmailStr

class User(Document):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True
    
    class Settings:
        name = "users"  # Collection name in the database
