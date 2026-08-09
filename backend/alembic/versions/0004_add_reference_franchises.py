import sqlalchemy as sa

from alembic import op

revision = "0004_add_reference_franchises"
down_revision = "0003_add_media_and_franchises"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reference_franchises",
        sa.Column("reference_id", sa.Integer(), nullable=False),
        sa.Column("franchise_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["reference_id"],
            ["cultural_references.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["franchise_id"],
            ["franchises.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("reference_id", "franchise_id"),
    )


def downgrade() -> None:
    op.drop_table("reference_franchises")
