"""add column researchDirection to table employer

Revision ID: 4433060d36a2
Revises: dca7b9b63fef
Create Date: 2022-12-12 13:29:21.004281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4433060d36a2'
down_revision = 'dca7b9b63fef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('researchDirection', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employer', schema=None) as batch_op:
        batch_op.drop_column('researchDirection')

    # ### end Alembic commands ###
