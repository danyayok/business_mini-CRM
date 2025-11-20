from app.models.models import Deal
from app.repos.base import BaseRepo


class DealRepo(BaseRepo):
    def get_for_org(self, org_id, deal_id=None, filters=None):
        query = self.db.query(Deal).filter(Deal.organization_id == org_id)

        if deal_id:
            query = query.filter(Deal.id == deal_id)
            return query.first()

        if filters:
            if filters.get('status'):
                if isinstance(filters['status'], list):
                    query = query.filter(Deal.status.in_(filters['status']))
                else:
                    query = query.filter(Deal.status == filters['status'])
            if filters.get('stage'):
                query = query.filter(Deal.stage == filters['stage'])
            if filters.get('owner_id'):
                query = query.filter(Deal.owner_id == filters['owner_id'])
            if filters.get('min_amount'):
                query = query.filter(Deal.amount >= filters['min_amount'])
            if filters.get('max_amount'):
                query = query.filter(Deal.amount <= filters['max_amount'])

        return query.all()

    def get_by_contact(self, contact_id):
        return self.db.query(Deal).filter(Deal.contact_id == contact_id).all()