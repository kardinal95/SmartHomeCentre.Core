"""Added users and ACL

Revision ID: cd685b058c8e
Revises: ea8722305913
Create Date: 2019-12-04 17:03:38.037398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cd685b058c8e'
down_revision = 'ea8722305913'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('passhash', sa.Binary(), nullable=False),
    sa.Column('salt', sa.Binary(), nullable=False),
    sa.Column('acl', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    op.add_column('interface_params', sa.Column('read_acl', sa.Integer(), server_default='1', nullable=True))
    op.add_column('interface_params', sa.Column('write_acl', sa.Integer(), server_default='999', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('interface_params', 'write_acl')
    op.drop_column('interface_params', 'read_acl')
    op.drop_table('users')
    # ### end Alembic commands ###