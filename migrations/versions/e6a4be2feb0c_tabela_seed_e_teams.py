"""tabela seed e teams

Revision ID: e6a4be2feb0c
Revises: e0ffa1d6208c
Create Date: 2023-05-23 02:08:41.590618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6a4be2feb0c'
down_revision = 'e0ffa1d6208c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('round',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('seed',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_match', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seed_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'seed', ['seed_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('seed_id')

    op.drop_table('seed')
    op.drop_table('round')
    # ### end Alembic commands ###