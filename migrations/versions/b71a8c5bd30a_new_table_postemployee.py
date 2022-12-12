"""new table PostEmployee

Revision ID: b71a8c5bd30a
Revises: 133945b2b42b
Create Date: 2022-12-12 12:49:03.674036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b71a8c5bd30a'
down_revision = '133945b2b42b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post_employee',
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pid'], ['post.pid'], ),
    sa.ForeignKeyConstraint(['uid'], ['employee.uid'], ),
    sa.PrimaryKeyConstraint('pid', 'uid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_employee')
    # ### end Alembic commands ###