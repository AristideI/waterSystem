"""empty message

Revision ID: 8fdc0a31a021
Revises: 
Create Date: 2023-01-21 19:43:36.498433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fdc0a31a021'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('branch',
    sa.Column('branch_code', sa.String(length=5), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('branch_code')
    )
    op.create_table('customer',
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('firstname', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('district',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('province', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('customeCareOfficer',
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('firstname', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('branch_code', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['branch_code'], ['branch.branch_code'], ),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('headOfBranch',
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('firstname', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('branch_code', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['branch_code'], ['branch.branch_code'], ),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('sector',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('district_name', sa.String(length=80), nullable=True),
    sa.Column('branch_code', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['branch_code'], ['branch.branch_code'], ),
    sa.ForeignKeyConstraint(['district_name'], ['district.name'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('wateDistributionOfficer',
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('firstname', sa.String(length=80), nullable=True),
    sa.Column('lastname', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=15), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('branch_code', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['branch_code'], ['branch.branch_code'], ),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('cell',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('sector_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sector_id'], ['sector._id'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('clientRequest',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('province', sa.String(length=80), nullable=True),
    sa.Column('district', sa.String(length=80), nullable=True),
    sa.Column('sector', sa.String(length=80), nullable=True),
    sa.Column('cell', sa.String(length=80), nullable=True),
    sa.Column('village', sa.String(length=80), nullable=True),
    sa.Column('water_usage', sa.String(length=80), nullable=True),
    sa.Column('phone', sa.String(length=80), nullable=True),
    sa.Column('nid', sa.String(length=80), nullable=True),
    sa.Column('plotn', sa.String(length=80), nullable=True),
    sa.Column('nid_doc', sa.String(length=80), nullable=True),
    sa.Column('upi_doc', sa.String(length=80), nullable=True),
    sa.Column('payment', sa.String(length=80), nullable=True),
    sa.Column('request_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=80), nullable=True),
    sa.Column('customer_email', sa.String(length=80), nullable=True),
    sa.Column('branch_code', sa.String(length=5), nullable=True),
    sa.Column('cco_email', sa.String(length=80), nullable=True),
    sa.Column('wdo_email', sa.String(length=80), nullable=True),
    sa.Column('hob_email', sa.String(length=80), nullable=True),
    sa.ForeignKeyConstraint(['branch_code'], ['branch.branch_code'], ),
    sa.ForeignKeyConstraint(['cco_email'], ['customeCareOfficer.email'], ),
    sa.ForeignKeyConstraint(['customer_email'], ['customer.email'], ),
    sa.ForeignKeyConstraint(['hob_email'], ['headOfBranch.email'], ),
    sa.ForeignKeyConstraint(['wdo_email'], ['wateDistributionOfficer.email'], ),
    sa.PrimaryKeyConstraint('_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clientRequest')
    op.drop_table('cell')
    op.drop_table('wateDistributionOfficer')
    op.drop_table('sector')
    op.drop_table('headOfBranch')
    op.drop_table('customeCareOfficer')
    op.drop_table('district')
    op.drop_table('customer')
    op.drop_table('branch')
    # ### end Alembic commands ###