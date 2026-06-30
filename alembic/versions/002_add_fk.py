# alembic/versions/002_add_fk.py
"""add foreign key constraints

Revision ID: 002
Revises: 001
Create Date: 2026-07-02
"""

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    op.create_foreign_key(
        "fk_conversations_user_id",
        "conversations",
        "users",
        ["user_id"],
        ["id"],
        source_schema="poc",
        referent_schema="poc",
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "fk_messages_conversation_id",
        "messages",
        "conversations",
        ["conversation_id"],
        ["id"],
        source_schema="poc",
        referent_schema="poc",
        ondelete="CASCADE",
    )


def downgrade():
    op.drop_constraint(
        "fk_conversations_user_id", "conversations", schema="poc", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_messages_conversation_id", "messages", schema="poc", type_="foreignkey"
    )
