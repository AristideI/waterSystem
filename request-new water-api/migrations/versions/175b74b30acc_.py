"""empty message

Revision ID: 175b74b30acc
Revises: 8fdc0a31a021
Create Date: 2023-01-23 01:54:06.344758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '175b74b30acc'
down_revision = '8fdc0a31a021'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clientRequest', schema=None) as batch_op:
        batch_op.add_column(sa.Column('boq_doc', sa.String(length=80), nullable=True))
        batch_op.add_column(sa.Column('rej_reason', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clientRequest', schema=None) as batch_op:
        batch_op.drop_column('rej_reason')
        batch_op.drop_column('boq_doc')

    # ### end Alembic commands ###
