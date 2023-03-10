"""empty message

Revision ID: c41ec316092d
Revises: bb9853459602
Create Date: 2023-02-14 18:52:54.871883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c41ec316092d'
down_revision = 'bb9853459602'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('website', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('seeking_description', sa.String(length=120), nullable=True))
        batch_op.alter_column('seeking_venue',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.drop_column('seeking_venue_decription')

    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_description', sa.String(length=120), nullable=True))
        batch_op.alter_column('seeking_talent',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=120),
               existing_nullable=False)
        batch_op.drop_column('seeking_talent_decription')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Venue', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_talent_decription', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
        batch_op.alter_column('seeking_talent',
               existing_type=sa.String(length=120),
               type_=sa.BOOLEAN(),
               existing_nullable=False)
        batch_op.drop_column('seeking_description')

    with op.batch_alter_table('Artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('seeking_venue_decription', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
        batch_op.alter_column('seeking_venue',
               existing_type=sa.String(length=120),
               type_=sa.BOOLEAN(),
               existing_nullable=False)
        batch_op.drop_column('seeking_description')
        batch_op.drop_column('website')

    # ### end Alembic commands ###
