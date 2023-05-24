"""Migrate new model classification

Revision ID: 8f6bedbaba86
Revises: 9b90ac196bb3
Create Date: 2023-05-24 01:09:38.688271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f6bedbaba86'
down_revision = '9b90ac196bb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classification_score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('in_progress', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('classification_score')
    # ### end Alembic commands ###
