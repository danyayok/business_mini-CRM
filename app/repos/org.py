from app.models.models import Organization, OrganizationMember, User
from app.repos.base import BaseRepo
from sqlalchemy.orm import joinedload


class OrgRepo(BaseRepo):
    def create_org(self, name, user_id):
        org = self.create(Organization, {"name": name})
        self.create(OrganizationMember, {
            "organization_id": org.id,
            "user_id": user_id,
            "role": "owner"
        })
        return org

    def get_user_orgs(self, user_id):
        return self.db.query(Organization).join(OrganizationMember).filter(
            OrganizationMember.user_id == user_id
        ).all()

    def get_org_members(self, org_id):
        return self.db.query(OrganizationMember).filter(
            OrganizationMember.organization_id == org_id
        ).options(joinedload(OrganizationMember.user)).all()

    def get_org_member(self, org_id, user_id):
        return self.db.query(OrganizationMember).filter(
            OrganizationMember.organization_id == org_id,
            OrganizationMember.user_id == user_id
        ).first()

    def add_member(self, org_id, user_id, role):
        existing = self.get_org_member(org_id, user_id)
        if existing:
            return None

        return self.create(OrganizationMember, {
            "organization_id": org_id,
            "user_id": user_id,
            "role": role
        })

    def update_member_role(self, org_id, user_id, new_role):
        member = self.get_org_member(org_id, user_id)
        if member:
            return self.update(member, {"role": new_role})
        return None

    def remove_member(self, org_id, user_id):
        member = self.get_org_member(org_id, user_id)
        if member:
            # Нельзя удалить владельца организации
            if member.role == 'owner':
                return False
            self.delete(member)
            return True
        return False

    def get_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()