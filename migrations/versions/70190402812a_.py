"""empty message

Revision ID: 70190402812a
Revises: 
Create Date: 2021-05-12 01:15:45.868734

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70190402812a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('task_id', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('started', sa.DateTime(), nullable=True),
    sa.Column('finished', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_upload_task_id'), 'upload', ['task_id'], unique=False)
    op.create_table('point',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('upload_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.String(), nullable=False),
    sa.Column('longitude', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['upload_id'], ['upload.id'], ondelete='restrict'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('point_a_id', sa.Integer(), nullable=False),
    sa.Column('point_b_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('distance', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['point_a_id'], ['point.id'], ondelete='restrict'),
    sa.ForeignKeyConstraint(['point_b_id'], ['point.id'], ondelete='restrict'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('link')
    op.drop_table('point')
    op.drop_index(op.f('ix_upload_task_id'), table_name='upload')
    op.drop_table('upload')
    # ### end Alembic commands ###