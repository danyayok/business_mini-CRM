from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    owner_id: int
    organization_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)