"""remove test

Revision ID: 5bf73a7a50c3
Revises: 7e6fe4606f7e
Create Date: 2021-04-26 13:10:27.974320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bf73a7a50c3'
down_revision = '7e6fe4606f7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('discord_member_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('date_joined', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('test_column', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    # ### end Alembic commands ###
