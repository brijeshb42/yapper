"""empty message

Revision ID: 8d751abc3d0
Revises: 474983cdda83
Create Date: 2014-11-23 11:03:34.880000

"""

# revision identifiers, used by Alembic.
revision = '8d751abc3d0'
down_revision = '474983cdda83'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    ### end Alembic commands ###