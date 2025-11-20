import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import date, timedelta
from fastapi import HTTPException
from app.services.deal import DealService
from app.services.task import TaskService
from app.services.contact import ContactService
from decimal import Decimal
from app.models.models import Deal, Contact


def test_business_rules(db_session):

    print("=== Testing Deal Stage Validation ===")

    class MockMemberUser:
        def __init__(self):
            self.id = 1
            self.org_id = 1
            self.role = "member"

    class MockAdminUser:
        def __init__(self):
            self.id = 1
            self.org_id = 1
            self.role = "admin"

    member_user = MockMemberUser()
    member_deal_service = DealService(db_session, member_user)

    try:
        member_deal_service._validate_stage_change("proposal", "qualification")
        print("ERROR: Stage rollback should be blocked for members")
        assert False, "Stage rollback should have been blocked for members"
    except HTTPException as e:
        if "Cannot revert stage" in str(e):
            print("Stage rollback correctly blocked for members")
        else:
            print(f"Wrong error message: {e}")
            raise

    try:
        result = member_deal_service._validate_stage_change("qualification", "proposal")
        print("Stage progression allowed for members")
        assert result == True
    except Exception as e:
        print(f"Stage progression should be allowed: {e}")
        raise

    admin_user = MockAdminUser()
    admin_deal_service = DealService(db_session, admin_user)

    try:
        result = admin_deal_service._validate_stage_change("proposal", "qualification")
        print("Stage rollback allowed for admin")
        assert result == True
    except Exception as e:
        print(f"Stage rollback should be allowed for admin: {e}")
        raise

    print("=== Testing Task Validation ===")

    contact = Contact(
        organization_id=1,
        owner_id=1,
        name="Test Contact",
        email="test@test.com",
        phone="+123456789"
    )
    db_session.add(contact)
    db_session.commit()

    deal = Deal(
        organization_id=1,
        contact_id=contact.id,
        owner_id=1,
        title="Test Deal",
        amount=Decimal("1000.00"),
        currency="USD",
        status="new",
        stage="qualification"
    )
    db_session.add(deal)
    db_session.commit()

    task_service = TaskService(db_session, admin_user)

    try:
        class MockTaskData:
            def __init__(self, deal_id):
                self.deal_id = deal_id
                self.title = "Test"
                self.description = "Test description"
                self.due_date = date.today() - timedelta(days=1)

            def model_dump(self):
                return {
                    "deal_id": self.deal_id,
                    "title": self.title,
                    "description": self.description,
                    "due_date": self.due_date
                }

        task_data = MockTaskData(deal_id=deal.id)
        task_service.create(task_data)
        print("ERROR: Past due date should be blocked")
        assert False, "Should have raised exception for past due date"
    except HTTPException as e:
        if "Due date in past" in str(e):
            print("✅ Past due date correctly blocked")
        else:
            print(f"Wrong error message: {e}")
            raise

    print("All business rules validated!")


def test_deal_amount_validation(db_session):
    from app.schemas.deal import DealCreate
    from pydantic import ValidationError

    print("=== Testing Deal Amount Validation via Pydantic ===")

    try:
        deal_data = DealCreate(
            contact_id=1,
            title="Test Deal",
            amount=Decimal("0"),
            currency="USD"
        )
        print("ERROR: Zero amount should be blocked by Pydantic")
        assert False, "Zero amount should have been blocked by Pydantic"
    except ValidationError as e:
        if "Amount must be positive" in str(e):
            print("Zero amount correctly blocked by Pydantic")
        else:
            print(f"Wrong validation error: {e}")
            raise

    try:
        deal_data = DealCreate(
            contact_id=1,
            title="Test Deal",
            amount=Decimal("-100.00"),
            currency="USD"
        )
        print("ERROR: Negative amount should be blocked by Pydantic")
        assert False, "Negative amount should have been blocked by Pydantic"
    except ValidationError as e:
        if "Amount must be positive" in str(e):
            print("Negative amount correctly blocked by Pydantic")
        else:
            print(f"Wrong validation error: {e}")
            raise

    try:
        deal_data = DealCreate(
            contact_id=1,
            title="Test Deal",
            amount=Decimal("1000.00"),
            currency="USD"
        )
        print("Positive amount allowed by Pydantic")
        assert deal_data.amount == Decimal("1000.00")
    except ValidationError as e:
        print(f"Positive amount should be allowed: {e}")
        raise

    print("Deal amount validation via Pydantic works!")


def test_contact_deletion_validation(db_session):

    class MockUser:
        def __init__(self):
            self.id = 1
            self.org_id = 1
            self.role = "owner"

    contact_service = ContactService(db_session, MockUser())

    contact = Contact(
        organization_id=1,
        owner_id=1,
        name="Test Contact",
        email="test@test.com",
        phone="+123456789"
    )
    db_session.add(contact)
    db_session.commit()

    deal = Deal(
        organization_id=1,
        contact_id=contact.id,
        owner_id=1,
        title="Test Deal",
        amount=Decimal("1000.00"),
        currency="USD",
        status="new",
        stage="qualification"
    )
    db_session.add(deal)
    db_session.commit()

    try:
        contact_service.delete(contact.id)
        print("ERROR: Contact with active deals should not be deletable")
        assert False, "Contact with active deals should not be deletable"
    except HTTPException as e:
        if "Contact has active deals" in str(e):
            print("Contact deletion correctly blocked when has active deals")
        else:
            print(f"Wrong error message: {e}")
            raise

    db_session.delete(deal)
    db_session.commit()

    try:
        result = contact_service.delete(contact.id)
        print("Contact deletion allowed when no active deals")
        assert result["ok"] == True
    except Exception as e:
        print(f"Contact should be deletable when no deals: {e}")
        raise

    print("Contact deletion validation works!")


if __name__ == "__main__":
    print("Run with: pytest tests/test_business_rules.py -v -s")