import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi import HTTPException
from app.services.org import OrgService
from app.services.auth import AuthService
from app.services.deal import DealService
from app.core.security import verify_password, get_password_hash


def test_password_hashing():
    password = "test123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) == True
    assert verify_password("wrong", hashed) == False


def test_deal_service_validation(db_session):
    class MockUser:
        id = 1
        org_id = 1
        role = "member"

    current_user = MockUser()
    service = DealService(db_session, current_user)

    with pytest.raises(HTTPException) as exc:
        service._validate_stage_change("proposal", "qualification")
    assert exc.value.status_code == 400

    try:
        service._validate_stage_change("qualification", "proposal")
    except HTTPException:
        pytest.fail("Valid stage change should not raise exception")


def test_org_service_add_member(db_session):
    auth_service = AuthService(db_session)

    owner_result = auth_service.register("owner@org.com", "pass123", "Owner", "Test Org")

    member_result = auth_service.register("member@org.com", "pass123", "Member", "Other Org")

    class MockCurrentUser:
        def __init__(self, user_id, org_id, role):
            self.id = user_id
            self.org_id = org_id
            self.role = role

    current_user = MockCurrentUser(
        user_id=owner_result["user_id"],
        org_id=owner_result["org"]["id"],
        role="owner"
    )

    org_service = OrgService(db_session, current_user)

    result = org_service.add_member(owner_result["org"]["id"], "member@org.com", "manager")
    assert result is not None
    assert result["role"] == "manager"
    assert result["user_email"] == "member@org.com"

    with pytest.raises(HTTPException) as exc:
        org_service.add_member(owner_result["org"]["id"], "member@org.com", "member")
    assert exc.value.status_code == 409

    print("Org service member management test passed!")