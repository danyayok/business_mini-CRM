from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.deps import get_current_user, CurrentUser
from app.schemas.deal import DealCreate, DealUpdate, DealOut
from app.services.deal import DealService

router = APIRouter(prefix="/deals")

@router.get("/", response_model=list[DealOut])
def get_deals(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    status: list[str] = Query(None),
    stage: str = Query(None),
    owner_id: int = Query(None),
    min_amount: float = Query(None),
    max_amount: float = Query(None)
):
    service = DealService(db, current_user)
    filters = {"status": status, "stage": stage, "owner_id": owner_id, "min_amount": min_amount, "max_amount": max_amount}
    return service.get_all(filters)

@router.post("/", response_model=DealOut)
def create_deal(
    data: DealCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = DealService(db, current_user)
    return service.create(data)

@router.patch("/{deal_id}", response_model=DealOut)
def update_deal(
    deal_id: int,
    data: DealUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = DealService(db, current_user)
    return service.update(deal_id, data)