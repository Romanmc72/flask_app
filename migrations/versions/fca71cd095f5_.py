"""empty message

Revision ID: fca71cd095f5
Revises: 3684854c2f86
Create Date: 2021-02-27 10:31:06.741818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fca71cd095f5'
down_revision = '3684854c2f86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('token_used', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    schema='flask_app'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_flask_app_score_score'), table_name='score', schema='flask_app')
    op.drop_table('score', schema='flask_app')
    # ### end Alembic commands ###