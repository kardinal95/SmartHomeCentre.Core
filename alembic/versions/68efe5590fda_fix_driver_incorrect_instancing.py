"""fix driver incorrect instancing

Revision ID: 68efe5590fda
Revises: 0abf2310d649
Create Date: 2019-09-11 19:46:18.545171

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '68efe5590fda'
down_revision = '0abf2310d649'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mqtt_endpoints', sa.Column('parent_uuid', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'mqtt_endpoints', 'driver_instances', ['parent_uuid'], ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mqtt_endpoints', type_='foreignkey')
    op.drop_column('mqtt_endpoints', 'parent_uuid')
    # ### end Alembic commands ###
