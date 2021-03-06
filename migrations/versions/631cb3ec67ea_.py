"""empty message

Revision ID: 631cb3ec67ea
Revises: e4b159e18385
Create Date: 2022-03-17 09:08:19.459512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '631cb3ec67ea'
down_revision = 'e4b159e18385'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vm', sa.Column('ativo_dias', sa.Integer(), nullable=False))
    op.add_column('vm', sa.Column('ativo_horas', sa.Integer(), nullable=False))
    op.add_column('vm', sa.Column('total_ativo_dias', sa.Integer(), nullable=False))
    op.add_column('vm', sa.Column('total_ativo_horas', sa.Integer(), nullable=False))
    op.add_column('vm', sa.Column('desativada', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vm', 'desativada')
    op.drop_column('vm', 'total_ativo_horas')
    op.drop_column('vm', 'total_ativo_dias')
    op.drop_column('vm', 'ativo_horas')
    op.drop_column('vm', 'ativo_dias')
    # ### end Alembic commands ###
