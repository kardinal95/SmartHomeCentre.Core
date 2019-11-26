"""Trigger param fix

Revision ID: dd0acf882385
Revises: ee36b03b1adf
Create Date: 2019-11-19 14:21:21.876608

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'dd0acf882385'
down_revision = 'ee36b03b1adf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trigger_params', sa.Column('trigger_uuid', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'trigger_params', 'triggers', ['trigger_uuid'], ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trigger_params', type_='foreignkey')
    op.drop_column('trigger_params', 'trigger_uuid')
    # ### end Alembic commands ###