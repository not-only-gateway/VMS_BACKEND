"""Migrar

Revision ID: ef33d741b93d
Revises: 835c2007c584
Create Date: 2022-04-01 10:10:56.637575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef33d741b93d'
down_revision = '835c2007c584'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('volume',
    sa.Column('codigo_id', sa.BigInteger(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('pure_id', sa.String(), nullable=False),
    sa.Column('espaco', sa.BigInteger(), nullable=False),
    sa.Column('espaco_usado', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('codigo_id'),
    sa.UniqueConstraint('nome'),
    sa.UniqueConstraint('pure_id')
    )
    op.add_column('host', sa.Column('cluster', sa.String(), nullable=True))
    op.add_column('host', sa.Column('volume', sa.String(), nullable=True))
    op.create_foreign_key(None, 'host', 'volume', ['volume'], ['codigo_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'host', type_='foreignkey')
    op.drop_column('host', 'volume')
    op.drop_column('host', 'cluster')
    op.drop_table('volume')
    # ### end Alembic commands ###
