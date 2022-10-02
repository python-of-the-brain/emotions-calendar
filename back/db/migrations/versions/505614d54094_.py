"""empty message

Revision ID: 505614d54094
Revises: 1a37addf2c9d
Create Date: 2022-10-01 17:13:47.916883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '505614d54094'
down_revision = '1a37addf2c9d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emotion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('src', sa.String(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__emotion'))
    )
    op.create_index(op.f('ix__emotion__id'), 'emotion', ['id'], unique=False)
    op.create_index(op.f('ix__emotion__name'), 'emotion', ['name'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('emotion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['emotion_id'], ['emotion.id'], name=op.f('fk__post__emotion_id__emotion')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk__post__user_id__user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__post'))
    )
    op.create_index(op.f('ix__post__emotion_id'), 'post', ['emotion_id'], unique=False)
    op.create_index(op.f('ix__post__id'), 'post', ['id'], unique=False)
    op.create_index(op.f('ix__post__user_id'), 'post', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix__post__user_id'), table_name='post')
    op.drop_index(op.f('ix__post__id'), table_name='post')
    op.drop_index(op.f('ix__post__emotion_id'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix__emotion__name'), table_name='emotion')
    op.drop_index(op.f('ix__emotion__id'), table_name='emotion')
    op.drop_table('emotion')
    # ### end Alembic commands ###
