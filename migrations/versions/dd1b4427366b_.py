"""empty message

Revision ID: dd1b4427366b
Revises: 97949345ad84
Create Date: 2021-04-10 11:29:36.364577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd1b4427366b'
down_revision = '97949345ad84'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('temp_start', sa.Numeric(precision=16, scale=6), nullable=True), schema='flask_app')
    op.add_column('user', sa.Column('temp_end', sa.Numeric(precision=16, scale=6), nullable=True), schema='flask_app')
    op.alter_column('user', 'username', nullable=False, schema='flask_app')
    op.alter_column('user', 'email', nullable=False, schema='flask_app')
    op.alter_column('user', 'password_hash', nullable=False, schema='flask_app')
    op.alter_column('user', 'created_at', nullable=False, schema='flask_app')
    op.alter_column('user', 'last_modified_at', nullable=False, schema='flask_app')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', sa.Column('temp_start', sa.Numeric(precision=16, scale=6), nullable=True), schema='flask_app')
    op.drop_column('user', sa.Column('temp_end', sa.Numeric(precision=16, scale=6), nullable=True), schema='flask_app')
    op.alter_column('user', 'username', nullable=True, schema='flask_app')
    op.alter_column('user', 'email', nullable=True, schema='flask_app')
    op.alter_column('user', 'password_hash', nullable=True, schema='flask_app')
    op.alter_column('user', 'created_at', nullable=True, schema='flask_app')
    op.alter_column('user', 'last_modified_at', nullable=True, schema='flask_app')
    # ### end Alembic commands ###
