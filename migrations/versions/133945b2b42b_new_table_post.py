"""new table Post

Revision ID: 133945b2b42b
Revises: c05fd28c294b
Create Date: 2022-12-12 12:47:08.975901

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '133945b2b42b'
down_revision = 'c05fd28c294b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('pid', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('salary', sa.Integer(), nullable=False),
    sa.Column('degree', sa.String(length=50), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('tasks', sa.String(length=1000), nullable=False),
    sa.Column('requirements', sa.String(length=1000), nullable=False),
    sa.Column('inRecruitment', sa.Boolean(), nullable=False),
    sa.Column('employerId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employerId'], ['employer.uid'], ),
    sa.PrimaryKeyConstraint('pid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    # ### end Alembic commands ###
