"""users table

Revision ID: c79de899c22b
Revises: 2eda29a60246
Create Date: 2025-03-01 20:02:42.513205

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c79de899c22b"
down_revision = "2eda29a60246"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    with op.batch_alter_table("Users", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_Users_username"), ["username"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("Users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_Users_username"))

    op.drop_table("Users")
    # ### end Alembic commands ###
