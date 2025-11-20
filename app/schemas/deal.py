from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from decimal import Decimal
from typing import Optional


class DealCreate(BaseModel):
    contact_id: int
    title: str
    amount: Decimal
    currency: str

    @field_validator('amount')
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v

    @field_validator('currency')
    @classmethod
    def currency_valid(cls, v):
        if v not in ['USD', 'EUR', 'RUB']:
            raise ValueError('Invalid currency')
        return v


class DealUpdate(BaseModel):
    status: Optional[str] = None
    stage: Optional[str] = None

    @field_validator('status')
    @classmethod
    def status_valid(cls, v):
        if v and v not in ['new', 'in_progress', 'won', 'lost']:
            raise ValueError('Invalid status')
        return v

    @field_validator('stage')
    @classmethod
    def stage_valid(cls, v):
        if v and v not in ['qualification', 'proposal', 'negotiation', 'closed']:
            raise ValueError('Invalid stage')
        return v


class DealOut(BaseModel):
    id: int
    title: str
    amount: Decimal
    currency: str
    status: str
    stage: str
    contact_id: int
    owner_id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)