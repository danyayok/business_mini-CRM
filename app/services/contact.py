from fastapi import HTTPException
from app.models.models import Contact  # Добавлен импорт
from app.repos.contact import ContactRepo
from app.repos.deal import DealRepo


class ContactService:
    def __init__(self, db, current_user):
        self.db = db
        self.user_id = current_user.id
        self.org_id = current_user.org_id
        self.role = current_user.role
        self.repo = ContactRepo(db)
        self.deal_repo = DealRepo(db)

    def get_all(self, filters):
        if self.role in ['owner', 'admin', 'manager']:
            return self.repo.get_for_org(self.org_id, filters=filters)
        else:
            filters['owner_id'] = self.user_id
            return self.repo.get_for_org(self.org_id, filters=filters)

    def create(self, data):
        contact_data = {
            **data.model_dump(),
            "organization_id": self.org_id,
            "owner_id": self.user_id
        }
        return self.repo.create(Contact, contact_data)

    def delete(self, contact_id):
        contact = self.repo.get_for_org(self.org_id, contact_id=contact_id)
        if not contact:
            raise HTTPException(404, "Contact not found")

        deals = self.deal_repo.get_by_contact(contact_id)
        if deals:
            raise HTTPException(409, "Contact has active deals")

        if self.role == 'member' and contact.owner_id != self.user_id:
            raise HTTPException(403, "No access")

        self.repo.delete(contact)
        return {"ok": True}