"""Init

Revision ID: 8df2b706e02f
Revises: 
Create Date: 2023-02-19 00:24:08.684567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8df2b706e02f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Contacts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('surname', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('phone', sa.String(length=19), nullable=True),
    sa.Column('b_date', sa.Date(), nullable=True),
    sa.Column('additional_info', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Contacts_id'), 'Contacts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Contacts_id'), table_name='Contacts')
    op.drop_table('Contacts')
    # ### end Alembic commands ###
