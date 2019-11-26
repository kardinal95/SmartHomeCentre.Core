"""Fix triggers a bit

Revision ID: b2aec60d1af7
Revises: b3485667d74e
Create Date: 2019-11-19 14:07:03.784398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b2aec60d1af7'
down_revision = 'b3485667d74e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trigger_params',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('parameter_name', sa.String(length=64), nullable=False),
    sa.Column('parameter_value', sa.String(length=128), nullable=False),
    sa.Column('parameter_type', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_unique_constraint(None, 'scenarios', ['uuid'])
    op.create_unique_constraint(None, 'triggers', ['uuid'])
    op.drop_constraint('triggers_device_uuid_fkey', 'triggers', type_='foreignkey')
    op.drop_column('triggers', 'parameter_name')
    op.drop_column('triggers', 'device_uuid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('triggers', sa.Column('device_uuid', postgresql.UUID(), autoincrement=False, nullable=True))
    op.add_column('triggers', sa.Column('parameter_name', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.create_foreign_key('triggers_device_uuid_fkey', 'triggers', 'devices', ['device_uuid'], ['uuid'])
    op.drop_constraint(None, 'triggers', type_='unique')
    op.drop_constraint(None, 'scenarios', type_='unique')
    op.drop_table('trigger_params')
    # ### end Alembic commands ###
