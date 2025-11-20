from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.deps import get_current_user, CurrentUser
from app.schemas.contact import ContactCreate, ContactOut
from app.services.contact import ContactService

router = APIRouter(prefix="/contacts")

@router.get("/", response_model=list[ContactOut])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    search: str = Query(None),
    owner_id: int = Query(None)
):
    service = ContactService(db, current_user)
    filters = {"search": search, "owner_id": owner_id}
    return service.get_all(filters)

@router.post("/", response_model=ContactOut)
def create_contact(
    data: ContactCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = ContactService(db, current_user)
    return service.create(data)

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = ContactService(db, current_user)
    return service.delete(contact_id)