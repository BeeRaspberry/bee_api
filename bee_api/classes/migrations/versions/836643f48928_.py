"""empty message

Revision ID: 836643f48928
Revises: b431043ff42f
Create Date: 2018-07-29 17:17:11.504132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '836643f48928'
down_revision = 'b431043ff42f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hive', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('hive', sa.Column('last_update', sa.DateTime(), nullable=True))
    op.drop_column('hive', 'lastUpdate')
    op.drop_column('hive', 'dateCreated')
    op.add_column('hiveData', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.drop_column('hiveData', 'dateCreated')
    op.add_column('location', sa.Column('postal_code', sa.String(length=20), nullable=True))
    op.add_column('location', sa.Column('street_address', sa.String(length=200), nullable=True))
    op.drop_column('location', 'streetAddress')
    op.drop_column('location', 'postalCode')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('postalCode', sa.VARCHAR(length=20), nullable=True))
    op.add_column('location', sa.Column('streetAddress', sa.VARCHAR(length=200), nullable=True))
    op.drop_column('location', 'street_address')
    op.drop_column('location', 'postal_code')
    op.add_column('hiveData', sa.Column('dateCreated', sa.DATETIME(), nullable=True))
    op.drop_column('hiveData', 'date_created')
    op.add_column('hive', sa.Column('dateCreated', sa.DATETIME(), nullable=True))
    op.add_column('hive', sa.Column('lastUpdate', sa.DATETIME(), nullable=True))
    op.drop_column('hive', 'last_update')
    op.drop_column('hive', 'date_created')
    # ### end Alembic commands ###