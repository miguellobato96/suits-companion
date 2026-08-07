from alembic import op
import sqlalchemy as sa


revision = "0003_add_media_and_franchises"
down_revision = "0002_add_timestamps"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "franchises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_index(
        op.f("ix_franchises_id"),
        "franchises",
        ["id"],
        unique=False,
    )

    op.create_table(
        "media",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("media_type", sa.String(length=50), nullable=False),
        sa.Column("release_year", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_media_id"),
        "media",
        ["id"],
        unique=False,
    )

    op.create_table(
        "media_franchises",
        sa.Column("media_id", sa.Integer(), nullable=False),
        sa.Column("franchise_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["media_id"],
            ["media.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["franchise_id"],
            ["franchises.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("media_id", "franchise_id"),
    )

    op.create_table(
        "reference_media",
        sa.Column("reference_id", sa.Integer(), nullable=False),
        sa.Column("media_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["reference_id"],
            ["cultural_references.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["media_id"],
            ["media.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("reference_id", "media_id"),
    )

    op.add_column(
        "cultural_references",
        sa.Column("quote", sa.Text(), nullable=True),
    )

    op.drop_column("cultural_references", "external_url")


def downgrade() -> None:
    op.add_column(
        "cultural_references",
        sa.Column("external_url", sa.String(length=500), nullable=True),
    )

    op.drop_column("cultural_references", "quote")

    op.drop_table("reference_media")
    op.drop_table("media_franchises")

    op.drop_index(op.f("ix_media_id"), table_name="media")
    op.drop_table("media")

    op.drop_index(op.f("ix_franchises_id"), table_name="franchises")
    op.drop_table("franchises")