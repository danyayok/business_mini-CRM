from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.deps import get_current_user, CurrentUser
from app.repos.activity import ActivityRepo
from app.schemas.activity import ActivityCreate, ActivityOut

router = APIRouter()

@router.get("/deals/{deal_id}/activities", response_model=list[ActivityOut])
def get_activities(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    repo = ActivityRepo(db)
    return repo.get_for_deal(deal_id)

@router.post("/deals/{deal_id}/activities", response_model=ActivityOut)
def create_activity(
    deal_id: int,
    data: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    repo = ActivityRepo(db)
    activity_data = {
        "deal_id": deal_id,
        "author_id": current_user.id,
        "type": data.type,
        "payload": data.payload
    }
    return repo.create(activity_data)