from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_token, decode_token
from app.repos.user import UserRepo
from app.repos.org import OrgRepo
from app.models.models import User, Organization


class AuthService:
    def __init__(self, db):
        self.user_repo = UserRepo(db)
        self.org_repo = OrgRepo(db)

    def register(self, email: str, password: str, name: str, org_name: str):
        if self.user_repo.get_by_email(email):
            raise HTTPException(400, "Email already exists")

        # вообще тут вроде была ошибка с версией bycrypt, но на всякий пусть будет
        if len(password) > 70:
            raise HTTPException(400, "Password too long")

        user = self.user_repo.create(User, {
            "email": email,
            "hashed_password": get_password_hash(password),
            "name": name
        })

        org = self.org_repo.create_org(org_name, user.id)

        return {
            "token": create_token({"sub": str(user.id)}),
            "user_id": user.id,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "org": {
                "id": org.id,
                "name": org.name
            }
        }

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Invalid credentials")

        return {
            "token": create_token({"sub": str(user.id)}),
            "user_id": user.id
        }