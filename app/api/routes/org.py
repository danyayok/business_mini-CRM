from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.deps import get_current_user, CurrentUser
from app.schemas.org import OrgOut, MemberCreate, MemberOut, MemberUpdate
from app.services.org import OrgService

router = APIRouter(prefix="/organizations")

@router.get("/me", response_model=list[OrgOut])
def get_my_orgs(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    from app.repos.org import OrgRepo
    repo = OrgRepo(db)
    return repo.get_user_orgs(current_user.id)

@router.get("/{org_id}/members", response_model=list[MemberOut])
def get_org_members(
    org_id: int = Path(..., description="Organization ID"),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = OrgService(db, current_user)
    return service.get_members(org_id)

@router.post("/{org_id}/members", response_model=MemberOut)
def add_member(
    data: MemberCreate,
    org_id: int = Path(..., description="Organization ID"),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = OrgService(db, current_user)
    return service.add_member(org_id, data.user_email, data.role)

@router.patch("/{org_id}/members/{user_id}", response_model=MemberOut)
def update_member_role(
    data: MemberUpdate,
    org_id: int = Path(..., description="Organization ID"),
    user_id: int = Path(..., description="User ID to update"),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = OrgService(db, current_user)
    return service.update_member_role(org_id, user_id, data.role)

@router.delete("/{org_id}/members/{user_id}")
def remove_member(
    org_id: int = Path(..., description="Organization ID"),
    user_id: int = Path(..., description="User ID to remove"),
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = OrgService(db, current_user)
    return service.remove_member(org_id, user_id)