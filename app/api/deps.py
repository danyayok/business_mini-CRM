from dataclasses import dataclass
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security import decode_token
from app.repos.user import UserRepo
from app.models.models import OrganizationMember, User


@dataclass
class CurrentUser:
    id: int
    email: str
    name: str
    role: str
    org_id: int

    def __init__(self, id: int, email: str, name: str, role: str, org_id: int):
        self.id = id
        self.email = email
        self.name = name
        self.role = role
        self.org_id = org_id


def get_current_user(
        db: Session = Depends(get_db),
        authorization: str = Header(..., alias="Authorization"),
        x_organization_id: int = Header(..., alias="X-Organization-Id")
) -> CurrentUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid token format")

    token = authorization[7:]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")

    user_id = int(payload.get("sub"))
    user_repo = UserRepo(db)
    user = user_repo.get(user_id)
    if not user:
        raise HTTPException(401, "User not found")

    member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == x_organization_id,
        OrganizationMember.user_id == user_id
    ).first()

    if not member:
        raise HTTPException(403, "Not a member of this organization")

    return CurrentUser(
        id=user.id,
        email=user.email,
        name=user.name,
        role=member.role,
        org_id=x_organization_id
    )