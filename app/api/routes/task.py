from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.api.deps import get_current_user, CurrentUser
from app.schemas.task import TaskCreate, TaskOut
from app.services.task import TaskService

router = APIRouter(prefix="/tasks")

@router.get("/", response_model=list[TaskOut])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
    deal_id: int = Query(None),
    only_open: bool = Query(False)
):
    service = TaskService(db, current_user)
    filters = {"deal_id": deal_id, "only_open": only_open}
    return service.get_all(filters)

@router.post("/", response_model=TaskOut)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    service = TaskService(db, current_user)
    return service.create(data)