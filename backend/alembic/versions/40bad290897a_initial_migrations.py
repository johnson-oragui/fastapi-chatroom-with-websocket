"""initial migrations

Revision ID: 40bad290897a
Revises: 
Create Date: 2024-09-21 18:38:59.558089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40bad290897a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    schema='public'
    )
    op.create_index(op.f('ix_public_users_created_at'), 'users', ['created_at'], unique=False, schema='public')
    op.create_index(op.f('ix_public_users_id'), 'users', ['id'], unique=False, schema='public')
    op.create_table('rooms',
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('owner_id', sa.String(length=60), nullable=False),
    sa.Column('is_private', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['public.users.id'], name=op.f('fk_rooms_owner_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rooms')),
    schema='public'
    )
    op.create_index(op.f('ix_public_rooms_created_at'), 'rooms', ['created_at'], unique=False, schema='public')
    op.create_index(op.f('ix_public_rooms_id'), 'rooms', ['id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_rooms_owner_id'), 'rooms', ['owner_id'], unique=False, schema='public')
    op.create_table('messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('room_id', sa.String(length=60), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=False),
    sa.Column('chat_type', sa.String(length=30), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['public.rooms.id'], name=op.f('fk_messages_room_id_rooms'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['public.users.id'], name=op.f('fk_messages_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages')),
    schema='public'
    )
    op.create_index(op.f('ix_public_messages_created_at'), 'messages', ['created_at'], unique=False, schema='public')
    op.create_index(op.f('ix_public_messages_id'), 'messages', ['id'], unique=True, schema='public')
    op.create_index(op.f('ix_public_messages_room_id'), 'messages', ['room_id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_messages_user_id'), 'messages', ['user_id'], unique=False, schema='public')
    op.create_table('room_members',
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('room_id', sa.String(length=60), nullable=False),
    sa.Column('invited_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['public.rooms.id'], name=op.f('fk_room_members_room_id_rooms'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['public.users.id'], name=op.f('fk_room_members_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_room_members')),
    sa.UniqueConstraint('room_id', 'user_id', name='uq_room_member_room_id_user_id'),
    schema='public'
    )
    op.create_index(op.f('ix_public_room_members_created_at'), 'room_members', ['created_at'], unique=False, schema='public')
    op.create_index(op.f('ix_public_room_members_id'), 'room_members', ['id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_room_members_room_id'), 'room_members', ['room_id'], unique=False, schema='public')
    op.create_index(op.f('ix_public_room_members_user_id'), 'room_members', ['user_id'], unique=False, schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_public_room_members_user_id'), table_name='room_members', schema='public')
    op.drop_index(op.f('ix_public_room_members_room_id'), table_name='room_members', schema='public')
    op.drop_index(op.f('ix_public_room_members_id'), table_name='room_members', schema='public')
    op.drop_index(op.f('ix_public_room_members_created_at'), table_name='room_members', schema='public')
    op.drop_table('room_members', schema='public')
    op.drop_index(op.f('ix_public_messages_user_id'), table_name='messages', schema='public')
    op.drop_index(op.f('ix_public_messages_room_id'), table_name='messages', schema='public')
    op.drop_index(op.f('ix_public_messages_id'), table_name='messages', schema='public')
    op.drop_index(op.f('ix_public_messages_created_at'), table_name='messages', schema='public')
    op.drop_table('messages', schema='public')
    op.drop_index(op.f('ix_public_rooms_owner_id'), table_name='rooms', schema='public')
    op.drop_index(op.f('ix_public_rooms_id'), table_name='rooms', schema='public')
    op.drop_index(op.f('ix_public_rooms_created_at'), table_name='rooms', schema='public')
    op.drop_table('rooms', schema='public')
    op.drop_index(op.f('ix_public_users_id'), table_name='users', schema='public')
    op.drop_index(op.f('ix_public_users_created_at'), table_name='users', schema='public')
    op.drop_table('users', schema='public')
    # ### end Alembic commands ###
