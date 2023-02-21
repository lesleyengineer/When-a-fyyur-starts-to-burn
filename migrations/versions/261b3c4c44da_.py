"""empty message

Revision ID: 261b3c4c44da
Revises: a953ab4da000
Create Date: 2023-02-15 17:45:54.707709

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '261b3c4c44da'
down_revision = 'a953ab4da000'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('genres', sa.String(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('seeking_venue', sa.String(length=120), nullable=False),
    sa.Column('seeking_description', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('artists')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('genres', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=False),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('seeking_venue', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('seeking_description', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='artists_venue_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='artists_pkey')
    )
    op.drop_table('Artists')
    # ### end Alembic commands ###