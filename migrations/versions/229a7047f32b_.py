"""empty message

Revision ID: 229a7047f32b
Revises: c51d31da7805
Create Date: 2021-07-20 03:48:55.223029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '229a7047f32b'
down_revision = 'c51d31da7805'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('Shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('Shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###