"""initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('hashed_password', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    op.create_index('ix_users_id', 'users', ['id'], unique=False)

    op.create_table('organizations',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_organizations_id', 'organizations', ['id'], unique=False)

    op.create_table('organization_members',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('role', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('organization_id', 'user_id', name='unique_org_user')
                    )
    op.create_index('ix_organization_members_id', 'organization_members', ['id'], unique=False)

    op.create_table('contacts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('phone', sa.String(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_contacts_id', 'contacts', ['id'], unique=False)

    op.create_table('deals',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('contact_id', sa.Integer(), nullable=False),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
                    sa.Column('currency', sa.String(), nullable=False),
                    sa.Column('status', sa.String(), server_default='new', nullable=False),
                    sa.Column('stage', sa.String(), server_default='qualification', nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
                    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_deals_id', 'deals', ['id'], unique=False)

    op.create_table('tasks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('deal_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('due_date', sa.DateTime(), nullable=False),
                    sa.Column('is_done', sa.Boolean(), server_default='false', nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['deal_id'], ['deals.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)

    op.create_table('activities',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('deal_id', sa.Integer(), nullable=False),
                    sa.Column('author_id', sa.Integer(), nullable=True),
                    sa.Column('type', sa.String(), nullable=False),
                    sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['deal_id'], ['deals.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index('ix_activities_id', 'activities', ['id'], unique=False)


def downgrade():
    op.drop_table('activities')
    op.drop_table('tasks')
    op.drop_table('deals')
    op.drop_table('contacts')
    op.drop_table('organization_members')
    op.drop_table('organizations')
    op.drop_table('users')
