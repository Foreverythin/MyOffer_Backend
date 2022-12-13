"""add comumn receivedResumes to table Post

Revision ID: 373ecca9ae25
Revises: 6c900c832353
Create Date: 2022-12-13 16:33:52.496103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '373ecca9ae25'
down_revision = '6c900c832353'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('receivedResumes', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('receivedResumes')

    # ### end Alembic commands ###
