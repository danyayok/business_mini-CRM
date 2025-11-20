from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Any

class ActivityCreate(BaseModel):
    type: str
    payload: dict

class ActivityOut(BaseModel):
    id: int
    deal_id: int
    author_id: Optional[int]
    type: str
    payload: dict
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)