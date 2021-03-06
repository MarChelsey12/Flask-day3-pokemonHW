"""empty message

Revision ID: 6703bc002a86
Revises: 
Create Date: 2022-02-16 16:11:16.361481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6703bc002a86'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('wins', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('losses', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'losses')
    op.drop_column('user', 'wins')
    # ### end Alembic commands ###
