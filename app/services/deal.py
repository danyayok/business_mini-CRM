from fastapi import HTTPException
from datetime import datetime
from app.models.models import Deal, Activity
from app.repos.deal import DealRepo
from app.repos.contact import ContactRepo
from app.repos.activity import ActivityRepo


class DealService:
    def __init__(self, db, current_user):
        self.db = db
        self.user_id = current_user.id
        self.org_id = current_user.org_id
        self.role = current_user.role
        self.repo = DealRepo(db)
        self.contact_repo = ContactRepo(db)
        self.activity_repo = ActivityRepo(db)

    def get_all(self, filters):
        if self.role in ['owner', 'admin', 'manager']:
            return self.repo.get_for_org(self.org_id, filters=filters)
        else:
            filters['owner_id'] = self.user_id
            return self.repo.get_for_org(self.org_id, filters=filters)

    def create(self, data):
        contact = self.contact_repo.get_for_org(self.org_id, contact_id=data.contact_id)
        if not contact:
            raise HTTPException(404, "Contact not found")

        deal_data = {
            **data.model_dump(),
            "organization_id": self.org_id,
            "owner_id": self.user_id,
            "status": "new",
            "stage": "qualification"
        }
        return self.repo.create(Deal, deal_data)

    def update(self, deal_id, data):
        deal = self.repo.get_for_org(self.org_id, deal_id=deal_id)
        if not deal:
            raise HTTPException(404, "Deal not found")

        if self.role == 'member' and deal.owner_id != self.user_id:
            raise HTTPException(403, "Can only edit own deals")

        if data.status == "won" and deal.amount <= 0:
            raise HTTPException(400, "Amount must be > 0 for won deals")

        old_stage = deal.stage
        if data.stage and data.stage != old_stage:
            self._validate_stage_change(old_stage, data.stage)
            self.activity_repo.create(Activity, {
                "deal_id": deal_id,
                "author_id": self.user_id,
                "type": "stage_changed",
                "payload": {"old": old_stage, "new": data.stage}
            })

        old_status = deal.status
        if data.status and data.status != old_status:
            self.activity_repo.create(Activity, {
                "deal_id": deal_id,
                "author_id": self.user_id,
                "type": "status_changed",
                "payload": {"old": old_status, "new": data.status}
            })

        return self.repo.update(deal, data.model_dump(exclude_unset=True))

    def _validate_stage_change(self, old, new):
        stages = ["qualification", "proposal", "negotiation", "closed"]
        old_idx = stages.index(old)
        new_idx = stages.index(new)

        if new_idx < old_idx and self.role in ['member', 'manager']:
            raise HTTPException(400, "Cannot revert stage")

    def _validate_stage_change(self, old, new):
        stages = ["qualification", "proposal", "negotiation", "closed"]

        if old == new:
            return True

        if old not in stages or new not in stages:
            raise HTTPException(400, f"Invalid stages: {old} -> {new}")

        old_idx = stages.index(old)
        new_idx = stages.index(new)

        print(f"DEBUG: {old}({old_idx}) -> {new}({new_idx}), role: {self.role}")

        if new_idx < old_idx:
            if self.role in ['member', 'manager']:
                raise HTTPException(400, "Cannot revert stage")

        return True