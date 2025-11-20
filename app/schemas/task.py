from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date, datetime
from typing import Optional


class TaskCreate(BaseModel):
    deal_id: int
    title: str
    description: Optional[str] = None
    due_date: date

    @field_validator('due_date')
    @classmethod
    def due_date_future(cls, v):
        if v < datetime.now().date():
            raise ValueError('Due date cannot be in past')
        return v


class TaskOut(BaseModel):
    id: int
    deal_id: int
    title: str
    description: Optional[str]
    due_date: date
    is_done: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)