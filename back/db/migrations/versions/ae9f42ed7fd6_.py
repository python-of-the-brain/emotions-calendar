"""empty message

Revision ID: ae9f42ed7fd6
Revises: 7266b1841dc1
Create Date: 2022-10-02 00:07:43.422153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae9f42ed7fd6'
down_revision = '7266b1841dc1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('comment', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('post', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('post', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('post', sa.Column('is_closed', sa.Boolean(), nullable=True))
    op.add_column('post', sa.Column('title', sa.String(length=256), nullable=False))
    op.add_column('post', sa.Column('content', sa.String(length=2048), nullable=False))
    op.create_index(op.f('ix__post__content'), 'post', ['content'], unique=False)
    op.create_index(op.f('ix__post__is_closed'), 'post', ['is_closed'], unique=False)
    op.create_index(op.f('ix__post__title'), 'post', ['title'], unique=False)
    op.add_column('status', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('status', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('status', sa.Column('is_closed', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix__status__is_closed'), 'status', ['is_closed'], unique=False)
    op.add_column('user', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True))
    op.add_column('user', sa.Column('is_closed', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix__user__is_closed'), 'user', ['is_closed'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__user__is_closed'), table_name='user')
    op.drop_column('user', 'is_closed')
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'created_at')
    op.drop_index(op.f('ix__status__is_closed'), table_name='status')
    op.drop_column('status', 'is_closed')
    op.drop_column('status', 'updated_at')
    op.drop_column('status', 'created_at')
    op.drop_index(op.f('ix__post__title'), table_name='post')
    op.drop_index(op.f('ix__post__is_closed'), table_name='post')
    op.drop_index(op.f('ix__post__content'), table_name='post')
    op.drop_column('post', 'content')
    op.drop_column('post', 'title')
    op.drop_column('post', 'is_closed')
    op.drop_column('post', 'updated_at')
    op.drop_column('post', 'created_at')
    op.drop_column('comment', 'updated_at')
    op.drop_column('comment', 'created_at')
    # ### end Alembic commands ###
