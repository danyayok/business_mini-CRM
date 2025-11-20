from app.models.models import Activity
from app.repos.base import BaseRepo

class ActivityRepo(BaseRepo):
    def get_for_deal(self, deal_id):
        return self.db.query(Activity).filter(Activity.deal_id == deal_id).all()