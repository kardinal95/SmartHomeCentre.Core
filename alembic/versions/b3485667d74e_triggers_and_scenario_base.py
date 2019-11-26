"""Triggers and scenario base

Revision ID: b3485667d74e
Revises: 0be4d9a4469a
Create Date: 2019-11-19 14:04:53.132792

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b3485667d74e'
down_revision = '0be4d9a4469a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scenarios',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('triggers',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('comment', sa.String(length=128), nullable=True),
    sa.Column('scenario_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('device_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('parameter_name', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['device_uuid'], ['devices.uuid'], ),
    sa.ForeignKeyConstraint(['scenario_uuid'], ['scenarios.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_unique_constraint(None, 'device_room_binds', ['uuid'])
    op.create_unique_constraint(None, 'rooms', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rooms', type_='unique')
    op.drop_constraint(None, 'device_room_binds', type_='unique')
    op.drop_table('triggers')
    op.drop_table('scenarios')
    # ### end Alembic commands ###