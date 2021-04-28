"""empty message

Revision ID: 9dc52c6a7cbb
Revises: c72184919554
Create Date: 2021-04-27 19:05:04.516165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9dc52c6a7cbb"
down_revision = "c72184919554"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "rlonesranks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("member_id", sa.BigInteger(), nullable=True),
        sa.Column("season", sa.Integer(), nullable=True),
        sa.Column("mmr", sa.Integer(), nullable=True),
        sa.Column("date_collected", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["member_id"],
            ["users.member_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rltwosranks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("member_id", sa.BigInteger(), nullable=True),
        sa.Column("season", sa.Integer(), nullable=True),
        sa.Column("mmr", sa.Integer(), nullable=True),
        sa.Column("date_collected", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["member_id"],
            ["users.member_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("rltwosranks")
    op.drop_table("rlonesranks")
    # ### end Alembic commands ###
