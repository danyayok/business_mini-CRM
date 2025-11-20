from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.deps import get_current_user, CurrentUser
from app.services.analytics import AnalyticsService
from app.schemas.analytics import DealSummary, DealFunnel

router = APIRouter()

@router.get("/deals/summary", response_model=DealSummary)
def deals_summary(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = AnalyticsService(db, current_user.org_id)
    return service.get_summary()

@router.get("/deals/funnel", response_model=DealFunnel)
def deals_funnel(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = AnalyticsService(db, current_user.org_id)
    return service.get_funnel()