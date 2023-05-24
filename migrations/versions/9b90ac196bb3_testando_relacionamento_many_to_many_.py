"""testando relacionamento many to many entre seed e teams

Revision ID: 9b90ac196bb3
Revises: 09bddaea5f96
Create Date: 2023-05-24 00:57:38.820568

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9b90ac196bb3'
down_revision = '09bddaea5f96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('team_has_seed',
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('seed_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['seed_id'], ['seed.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'seed_id')
    )
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.drop_constraint('team_ibfk_1', type_='foreignkey')
        batch_op.drop_column('seed_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('team', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seed_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('team_ibfk_1', 'seed', ['seed_id'], ['id'])

    op.drop_table('team_has_seed')
    # ### end Alembic commands ###
