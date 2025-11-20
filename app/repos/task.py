from app.models.models import Task, Deal
from app.repos.base import BaseRepo


class TaskRepo(BaseRepo):
    def get_for_org(self, org_id, filters=None):
        query = self.db.query(Task).join(Deal).filter(Deal.organization_id == org_id)

        if filters:
            if filters.get('deal_id'):
                query = query.filter(Task.deal_id == filters['deal_id'])
            if filters.get('only_open'):
                query = query.filter(Task.is_done == False)
            if filters.get('owner_id'):
                query = query.filter(Deal.owner_id == filters['owner_id'])

        return query.all()