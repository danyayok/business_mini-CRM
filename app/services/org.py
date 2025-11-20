from fastapi import HTTPException
from app.repos.org import OrgRepo
from app.repos.user import UserRepo


class OrgService:
    def __init__(self, db, current_user):
        self.db = db
        self.current_user = current_user
        self.repo = OrgRepo(db)
        self.user_repo = UserRepo(db)

    def get_members(self, org_id):
        user_member = self.repo.get_org_member(org_id, self.current_user.id)
        if not user_member:
            raise HTTPException(403, "No access to this organization")

        if user_member.role not in ['owner', 'admin', 'manager', 'member']:
            raise HTTPException(403, "Insufficient permissions")

        members = self.repo.get_org_members(org_id)

        result = []
        for member in members:
            result.append({
                "id": member.id,
                "user_id": member.user_id,
                "user_email": member.user.email,
                "user_name": member.user.name,
                "role": member.role,
                "organization_id": member.organization_id
            })

        return result

    def add_member(self, org_id, user_email, role):
        user_member = self.repo.get_org_member(org_id, self.current_user.id)
        if not user_member or user_member.role not in ['owner', 'admin']:
            raise HTTPException(403, "Only owners and admins can add members")

        valid_roles = ['admin', 'manager', 'member']
        if role not in valid_roles:
            raise HTTPException(400, f"Invalid role. Must be one of: {', '.join(valid_roles)}")

        user = self.repo.get_user_by_email(user_email)
        if not user:
            raise HTTPException(404, "User not found")

        if user.id == self.current_user.id:
            raise HTTPException(400, "Cannot add yourself as member")

        member = self.repo.add_member(org_id, user.id, role)
        if not member:
            raise HTTPException(409, "User is already a member of this organization")

        return {
            "id": member.id,
            "user_id": member.user_id,
            "user_email": user.email,
            "user_name": user.name,
            "role": member.role,
            "organization_id": member.organization_id
        }

    def update_member_role(self, org_id, member_user_id, new_role):
        user_member = self.repo.get_org_member(org_id, self.current_user.id)
        if not user_member or user_member.role not in ['owner', 'admin']:
            raise HTTPException(403, "Only owners and admins can change roles")

        valid_roles = ['admin', 'manager', 'member']
        if new_role not in valid_roles:
            raise HTTPException(400, f"Invalid role. Must be one of: {', '.join(valid_roles)}")

        target_member = self.repo.get_org_member(org_id, member_user_id)
        if not target_member:
            raise HTTPException(404, "Member not found")

        if target_member.role == 'owner':
            raise HTTPException(400, "Cannot change owner's role")

        if member_user_id == self.current_user.id and user_member.role == 'owner' and new_role != 'owner':
            raise HTTPException(400, "Owner cannot change their own role")

        updated_member = self.repo.update_member_role(org_id, member_user_id, new_role)
        if not updated_member:
            raise HTTPException(404, "Member not found")

        user = self.user_repo.get(member_user_id)
        return {
            "id": updated_member.id,
            "user_id": updated_member.user_id,
            "user_email": user.email,
            "user_name": user.name,
            "role": updated_member.role,
            "organization_id": updated_member.organization_id
        }

    def remove_member(self, org_id, member_user_id):
        user_member = self.repo.get_org_member(org_id, self.current_user.id)
        if not user_member or user_member.role not in ['owner', 'admin']:
            raise HTTPException(403, "Only owners and admins can remove members")

        if member_user_id == self.current_user.id:
            raise HTTPException(400, "Cannot remove yourself from organization")

        success = self.repo.remove_member(org_id, member_user_id)
        if not success:
            raise HTTPException(404, "Member not found or cannot be removed")

        return {"message": "Member removed successfully"}