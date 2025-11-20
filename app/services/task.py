from fastapi import HTTPException
from datetime import datetime
from app.models.models import Task  # Добавлен импорт
from app.repos.task import TaskRepo
from app.repos.deal import DealRepo


class TaskService:
    def __init__(self, db, current_user):
        self.db = db
        self.user_id = current_user.id
        self.org_id = current_user.org_id
        self.role = current_user.role
        self.repo = TaskRepo(db)
        self.deal_repo = DealRepo(db)

    def create(self, data):
        deal = self.deal_repo.get_for_org(self.org_id, deal_id=data.deal_id)
        if not deal:
            raise HTTPException(404, "Deal not found")

        if self.role == 'member' and deal.owner_id != self.user_id:
            raise HTTPException(403, "No access")

        if data.due_date < datetime.now().date():
            raise HTTPException(400, "Due date in past")

        task_data = data.model_dump()
        return self.repo.create(Task, task_data)

    def get_all(self, filters):
        if self.role in ['owner', 'admin', 'manager']:
            return self.repo.get_for_org(self.org_id, filters)
        else:
            filters['owner_id'] = self.user_id
            return self.repo.get_for_org(self.org_id, filters)