from app.models.models import User
from app.repos.base import BaseRepo

class UserRepo(BaseRepo):
    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get(self, id: int) -> User:
        return super().get(User, id)