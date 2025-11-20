from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

class OrgOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MemberCreate(BaseModel):
    user_email: EmailStr
    role: str

class MemberOut(BaseModel):
    id: int
    user_id: int
    user_email: str
    user_name: str
    role: str
    organization_id: int
    model_config = ConfigDict(from_attributes=True)

class MemberUpdate(BaseModel):
    role: str