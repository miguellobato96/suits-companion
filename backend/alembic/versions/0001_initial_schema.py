from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_schema"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "characters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column("actor", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_characters_id", "characters", ["id"], unique=False)

    op.create_table(
        "cultural_references",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("reference_type", sa.String(length=50), nullable=False),
        sa.Column("season", sa.Integer(), nullable=True),
        sa.Column("episode", sa.Integer(), nullable=True),
        sa.Column("context", sa.Text(), nullable=False),
        sa.Column("external_url", sa.String(length=500), nullable=True),
        sa.Column("spoken_by_character_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["spoken_by_character_id"], ["characters.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_cultural_references_id",
        "cultural_references",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_cultural_references_spoken_by_character_id",
        "cultural_references",
        ["spoken_by_character_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_cultural_references_spoken_by_character_id",
        table_name="cultural_references",
    )
    op.drop_index("ix_cultural_references_id", table_name="cultural_references")
    op.drop_table("cultural_references")

    op.drop_index("ix_characters_id", table_name="characters")
    op.drop_table("characters")