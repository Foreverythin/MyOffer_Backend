"""add column introduction to table employer

Revision ID: 6c900c832353
Revises: 4433060d36a2
Create Date: 2022-12-12 16:47:35.246583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c900c832353'
down_revision = '4433060d36a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('introduction', sa.String(length=1000), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employer', schema=None) as batch_op:
        batch_op.drop_column('introduction')

    # ### end Alembic commands ###
