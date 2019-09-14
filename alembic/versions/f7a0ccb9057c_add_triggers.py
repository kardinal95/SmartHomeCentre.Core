"""add triggers

Revision ID: f7a0ccb9057c
Revises: 7393ed925819
Create Date: 2019-09-11 18:26:53.805873

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f7a0ccb9057c'
down_revision = '7393ed925819'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('triggers',
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('source_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('scenario_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['scenario_uuid'], ['scenarios.uuid'], ),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('uuid')
    )
    op.create_unique_constraint(None, 'instruction_types', ['uuid'])
    op.create_unique_constraint(None, 'instructions', ['uuid'])
    op.create_unique_constraint(None, 'scenario_instructions', ['uuid'])
    op.create_unique_constraint(None, 'scenarios', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scenarios', type_='unique')
    op.drop_constraint(None, 'scenario_instructions', type_='unique')
    op.drop_constraint(None, 'instructions', type_='unique')
    op.drop_constraint(None, 'instruction_types', type_='unique')
    op.drop_table('triggers')
    # ### end Alembic commands ###