"""Starting point

Revision ID: 531f36e731cf
Revises: 
Create Date: 2019-11-19 13:20:09.040550

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '531f36e731cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('devices',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('driver_instances',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('driver_type', sa.Enum('mqtt', 'iface', name='drivertypeenum'), nullable=True),
    sa.Column('comment', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('mqtt_types',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('read_template', sa.String(length=256), nullable=False),
    sa.Column('write_template', sa.String(length=256), nullable=True),
    sa.Column('comment', sa.String(length=64), nullable=True),
    sa.Column('parameters', postgresql.JSON(none_as_null=256, astext_type=sa.Text()), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('driver_parameters',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('driver_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('param_name', sa.String(length=64), nullable=True),
    sa.Column('param_type', sa.String(length=64), nullable=True),
    sa.Column('param_value', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['driver_uuid'], ['driver_instances.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('endpoints',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('driver_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('driver_type', sa.Enum('mqtt', 'iface', name='drivertypeenum'), nullable=True),
    sa.ForeignKeyConstraint(['driver_uuid'], ['driver_instances.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('device_parameter_bindings',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('device_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('device_parameter', sa.String(length=64), nullable=False),
    sa.Column('endpoint_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('endpoint_parameter', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['device_uuid'], ['devices.uuid'], ),
    sa.ForeignKeyConstraint(['endpoint_uuid'], ['endpoints.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('interface_bindings',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('ep_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('ep_parameter', sa.String(length=64), nullable=False),
    sa.Column('device_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('device_parameter', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['device_uuid'], ['devices.uuid'], ),
    sa.ForeignKeyConstraint(['ep_uuid'], ['endpoints.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('interface_params',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('ep_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('type', sa.Enum('switch', 'rgb', 'display', name='interfaceeptypeenum'), nullable=True),
    sa.ForeignKeyConstraint(['ep_uuid'], ['endpoints.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('mqtt_params',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('ep_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('type_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('topic_read', sa.String(length=128), nullable=False),
    sa.Column('topic_write', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['ep_uuid'], ['endpoints.uuid'], ),
    sa.ForeignKeyConstraint(['type_uuid'], ['mqtt_types.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mqtt_params')
    op.drop_table('interface_params')
    op.drop_table('interface_bindings')
    op.drop_table('device_parameter_bindings')
    op.drop_table('endpoints')
    op.drop_table('driver_parameters')
    op.drop_table('mqtt_types')
    op.drop_table('driver_instances')
    op.drop_table('devices')
    # ### end Alembic commands ###
