"""empty message

Revision ID: 8927886b42d2
Revises: 9fd7a085319b
Create Date: 2021-07-22 00:44:42.992365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8927886b42d2'
down_revision = '9fd7a085319b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Shows', sa.Column('venue_id', sa.Integer(), nullable=True))
    op.add_column('Shows', sa.Column('artist_id', sa.Integer(), nullable=True))
    op.add_column('Shows', sa.Column('start_time', sa.String(length=120), nullable=True))
    op.create_foreign_key(None, 'Shows', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'Shows', 'Artist', ['artist_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_constraint(None, 'Shows', type_='foreignkey')
    op.drop_column('Shows', 'start_time')
    op.drop_column('Shows', 'artist_id')
    op.drop_column('Shows', 'venue_id')
    # ### end Alembic commands ###
