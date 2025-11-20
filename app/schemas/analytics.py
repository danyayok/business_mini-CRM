from pydantic import BaseModel, ConfigDict
from typing import Dict, List

class DealSummary(BaseModel):
    status_counts: Dict[str, int]
    status_amounts: Dict[str, float]
    avg_won_amount: float
    new_last_30_days: int

class FunnelStage(BaseModel):
    stage: str
    count: int
    conversion_from_previous: float

class DealFunnel(BaseModel):
    stages: List[FunnelStage]