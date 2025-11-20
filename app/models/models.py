from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Boolean, Text, JSON, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    organizations = relationship("OrganizationMember", back_populates="user")
    owned_contacts = relationship("Contact", back_populates="owner")
    owned_deals = relationship("Deal", back_populates="owner")
    activities = relationship("Activity", back_populates="author")


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("OrganizationMember", back_populates="organization")
    contacts = relationship("Contact", back_populates="organization")
    deals = relationship("Deal", back_populates="organization")


class OrganizationMember(Base):
    __tablename__ = "organization_members"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)

    organization = relationship("Organization", back_populates="members")
    user = relationship("User", back_populates="organizations")

    __table_args__ = (
        UniqueConstraint('organization_id', 'user_id', name='unique_org_user'),
    )


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    organization = relationship("Organization", back_populates="contacts")
    owner = relationship("User", back_populates="owned_contacts")
    deals = relationship("Deal", back_populates="contact")


class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    amount = Column(DECIMAL(10, 2))
    currency = Column(String)
    status = Column(String, default="new")
    stage = Column(String, default="qualification")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organization = relationship("Organization", back_populates="deals")
    contact = relationship("Contact", back_populates="deals")
    owner = relationship("User", back_populates="owned_deals")
    tasks = relationship("Task", back_populates="deal")
    activities = relationship("Activity", back_populates="deal")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    title = Column(String)
    description = Column(Text)
    due_date = Column(DateTime)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("Deal", back_populates="tasks")


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    deal_id = Column(Integer, ForeignKey("deals.id"))
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    type = Column(String)
    payload = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    deal = relationship("Deal", back_populates="activities")
    author = relationship("User", back_populates="activities")