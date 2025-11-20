from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional, Dict, Any


class RegisterReq(BaseModel):
    email: EmailStr
    password: str
    name: str
    organization_name: str

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str


class OrgResponse(BaseModel):
    id: int
    name: str


class Token(BaseModel):
    token: str
    user_id: int
    user: Optional[UserResponse] = None
    org: Optional[OrgResponse] = None


class RegisterResponse(BaseModel):
    token: str
    user_id: int
    user: UserResponse
    org: OrgResponse


class LoginResponse(BaseModel):
    token: str
    user_id: int