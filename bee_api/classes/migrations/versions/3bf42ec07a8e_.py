"""empty message

Revision ID: 3bf42ec07a8e
Revises: 
Create Date: 2018-07-26 19:56:55.238785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf42ec07a8e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stateProvince',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('countryId', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('abbreviation', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['countryId'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('streetAddress', sa.String(length=200), nullable=True),
    sa.Column('city', sa.String(length=200), nullable=True),
    sa.Column('stateProvinceId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['stateProvinceId'], ['stateProvince.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('firstName', sa.String(length=50), nullable=True),
    sa.Column('lastName', sa.String(length=50), nullable=True),
    sa.Column('phoneNumber', sa.String(length=20), nullable=True),
    sa.Column('locationId', sa.Integer(), nullable=True),
    sa.Column('registeredOn', sa.DateTime(), nullable=True),
    sa.Column('active', sa.BOOLEAN(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['locationId'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('hive',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ownerId', sa.Integer(), nullable=True),
    sa.Column('hiveId', sa.Integer(), nullable=True),
    sa.Column('locationId', sa.Integer(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.Column('lastUpdate', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['locationId'], ['location.id'], ),
    sa.ForeignKeyConstraint(['ownerId'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hiveData',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hiveId', sa.Integer(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.Column('temperature', sa.Numeric(), nullable=True),
    sa.Column('humidity', sa.Numeric(), nullable=True),
    sa.Column('sensor', sa.Integer(), nullable=True),
    sa.Column('outdoor', sa.BOOLEAN(), nullable=True),
    sa.ForeignKeyConstraint(['hiveId'], ['hive.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hiveData')
    op.drop_table('hive')
    op.drop_table('user')
    op.drop_table('location')
    op.drop_table('stateProvince')
    op.drop_table('role')
    op.drop_table('country')
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###
