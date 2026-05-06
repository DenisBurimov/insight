"""trgm_indexes_payments

Revision ID: a1b2c3d4e5f6
Revises: f70b41cc9fed
Create Date: 2026-05-06 00:00:00.000000

"""
from alembic import op


revision = 'a1b2c3d4e5f6'
down_revision = 'f70b41cc9fed'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_payments_payer_name_trgm "
        "ON payments USING gin (payer_name gin_trgm_ops)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_payments_recipient_name_trgm "
        "ON payments USING gin (recipient_name gin_trgm_ops)"
    )


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_payments_payer_name_trgm")
    op.execute("DROP INDEX IF EXISTS ix_payments_recipient_name_trgm")
