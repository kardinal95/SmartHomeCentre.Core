"""Fixed device-room binding

Revision ID: 3c4e31434950
Revises: 08418cb3e08b
Create Date: 2019-11-26 15:53:02.547077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c4e31434950'
down_revision = '08418cb3e08b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('device_room_binds_room_uuid_fkey', 'device_room_binds', type_='foreignkey')
    op.create_foreign_key(None, 'device_room_binds', 'rooms', ['room_uuid'], ['uuid'])
    op.create_unique_constraint(None, 'instructions', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'instructions', type_='unique')
    op.drop_constraint(None, 'device_room_binds', type_='foreignkey')
    op.create_foreign_key('device_room_binds_room_uuid_fkey', 'device_room_binds', 'endpoints', ['room_uuid'], ['uuid'])
    # ### end Alembic commands ###
