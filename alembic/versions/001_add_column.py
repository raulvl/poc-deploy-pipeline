# alembic/versions/001_add_column.py
"""add email to users

Revision ID: 001
Revises: None
Create Date: 2026-07-01
"""

revision = "001"
down_revision = None
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op


def upgrade():
    op.add_column(
        "users", sa.Column("email", sa.String(255), nullable=True), schema="poc"
    )


def downgrade():
    op.drop_column("users", "email", schema="poc")
