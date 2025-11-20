from app.models.models import Contact
from app.repos.base import BaseRepo


class ContactRepo(BaseRepo):
    def get_for_org(self, org_id, contact_id=None, filters=None):
        query = self.db.query(Contact).filter(Contact.organization_id == org_id)

        if contact_id:
            query = query.filter(Contact.id == contact_id)
            return query.first()

        if filters:
            if filters.get('owner_id'):
                query = query.filter(Contact.owner_id == filters['owner_id'])
            if filters.get('search'):
                search = f"%{filters['search']}%"
                query = query.filter(Contact.name.ilike(search) | Contact.email.ilike(search))

        return query.all()