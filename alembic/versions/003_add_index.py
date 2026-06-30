# alembic/versions/003_add_index.py
"""add index on messages.sent_at

Revision ID: 003
Revises: 002
Create Date: 2026-07-03
"""

revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None

from alembic import op


def upgrade():
    # CONCURRENTLY no puede correr dentro de una transacción.
    # Salimos del bloque, creamos el índice, y reabrimos para que Alembic registre la versión.
    op.execute("COMMIT")
    op.execute("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_messages_sent_at
        ON poc.messages (sent_at)
    """)
    op.execute("BEGIN")


def downgrade():
    op.execute("COMMIT")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS poc.idx_messages_sent_at")
    op.execute("BEGIN")
