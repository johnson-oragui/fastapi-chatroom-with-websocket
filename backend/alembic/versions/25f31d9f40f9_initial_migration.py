"""initial migration

Revision ID: 25f31d9f40f9
Revises: 
Create Date: 2024-10-03 11:49:10.660601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25f31d9f40f9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('idempotency_key', sa.String(length=120), nullable=False),
    sa.Column('email_verified', sa.Boolean(), nullable=False),
    sa.Column('status', sa.String(), server_default='active', nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('idempotency_key', name=op.f('uq_users_idempotency_key')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username')),
    schema='chat'
    )
    op.create_index(op.f('ix_chat_users_created_at'), 'users', ['created_at'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_users_id'), 'users', ['id'], unique=False, schema='chat')
    op.create_table('profiles',
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('recovery_email', sa.String(), nullable=True),
    sa.Column('bio', sa.String(length=500), nullable=True),
    sa.Column('profession', sa.String(length=50), nullable=True),
    sa.Column('avatar_url', sa.String(length=200), nullable=True),
    sa.Column('facebook_link', sa.String(length=200), nullable=True),
    sa.Column('x_link', sa.String(length=200), nullable=True),
    sa.Column('instagram_link', sa.String(length=200), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['chat.users.id'], name=op.f('fk_profiles_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_profiles')),
    schema='chat'
    )
    op.create_index(op.f('ix_chat_profiles_created_at'), 'profiles', ['created_at'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_profiles_id'), 'profiles', ['id'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_profiles_user_id'), 'profiles', ['user_id'], unique=True, schema='chat')
    op.create_table('rooms',
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('owner_id', sa.String(length=60), nullable=False),
    sa.Column('is_private', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['chat.users.id'], name=op.f('fk_rooms_owner_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_rooms')),
    schema='chat'
    )
    op.create_index(op.f('ix_chat_rooms_created_at'), 'rooms', ['created_at'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_rooms_id'), 'rooms', ['id'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_rooms_owner_id'), 'rooms', ['owner_id'], unique=False, schema='chat')
    op.create_table('social_logins',
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('provider', sa.String(), nullable=False),
    sa.Column('sub', sa.String(length=60), nullable=False),
    sa.Column('access_token', sa.String(), nullable=False),
    sa.Column('id_token', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['chat.users.id'], name=op.f('fk_social_logins_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_social_logins')),
    schema='chat'
    )
    op.create_index(op.f('ix_chat_social_logins_created_at'), 'social_logins', ['created_at'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_social_logins_id'), 'social_logins', ['id'], unique=False, schema='chat')
    op.create_table('messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('room_id', sa.String(length=60), nullable=False),
    sa.Column('content', sa.String(length=1000), nullable=False),
    sa.Column('chat_type', sa.String(length=30), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['chat.rooms.id'], name=op.f('fk_messages_room_id_rooms'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['chat.users.id'], name=op.f('fk_messages_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_messages')),
    schema='chat'
    )
    op.create_index(op.f('ix_chat_messages_created_at'), 'messages', ['created_at'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_messages_id'), 'messages', ['id'], unique=True, schema='chat')
    op.create_index(op.f('ix_chat_messages_room_id'), 'messages', ['room_id'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_messages_user_id'), 'messages', ['user_id'], unique=False, schema='chat')
    op.create_table('room_members',
    sa.Column('user_id', sa.String(length=60), nullable=False),
    sa.Column('room_id', sa.String(length=60), nullable=False),
    sa.Column('invited_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('id', sa.String(length=60), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['chat.rooms.id'], name=op.f('fk_room_members_room_id_rooms'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['chat.users.id'], name=op.f('fk_room_members_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_room_members')),
    sa.UniqueConstraint('room_id', 'user_id', name='uq_room_member_room_id_user_id'),
    schema='chat'
    )
    op.create_index(op.f('ix_chat_room_members_created_at'), 'room_members', ['created_at'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_room_members_id'), 'room_members', ['id'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_room_members_room_id'), 'room_members', ['room_id'], unique=False, schema='chat')
    op.create_index(op.f('ix_chat_room_members_user_id'), 'room_members', ['user_id'], unique=False, schema='chat')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_chat_room_members_user_id'), table_name='room_members', schema='chat')
    op.drop_index(op.f('ix_chat_room_members_room_id'), table_name='room_members', schema='chat')
    op.drop_index(op.f('ix_chat_room_members_id'), table_name='room_members', schema='chat')
    op.drop_index(op.f('ix_chat_room_members_created_at'), table_name='room_members', schema='chat')
    op.drop_table('room_members', schema='chat')
    op.drop_index(op.f('ix_chat_messages_user_id'), table_name='messages', schema='chat')
    op.drop_index(op.f('ix_chat_messages_room_id'), table_name='messages', schema='chat')
    op.drop_index(op.f('ix_chat_messages_id'), table_name='messages', schema='chat')
    op.drop_index(op.f('ix_chat_messages_created_at'), table_name='messages', schema='chat')
    op.drop_table('messages', schema='chat')
    op.drop_index(op.f('ix_chat_social_logins_id'), table_name='social_logins', schema='chat')
    op.drop_index(op.f('ix_chat_social_logins_created_at'), table_name='social_logins', schema='chat')
    op.drop_table('social_logins', schema='chat')
    op.drop_index(op.f('ix_chat_rooms_owner_id'), table_name='rooms', schema='chat')
    op.drop_index(op.f('ix_chat_rooms_id'), table_name='rooms', schema='chat')
    op.drop_index(op.f('ix_chat_rooms_created_at'), table_name='rooms', schema='chat')
    op.drop_table('rooms', schema='chat')
    op.drop_index(op.f('ix_chat_profiles_user_id'), table_name='profiles', schema='chat')
    op.drop_index(op.f('ix_chat_profiles_id'), table_name='profiles', schema='chat')
    op.drop_index(op.f('ix_chat_profiles_created_at'), table_name='profiles', schema='chat')
    op.drop_table('profiles', schema='chat')
    op.drop_index(op.f('ix_chat_users_id'), table_name='users', schema='chat')
    op.drop_index(op.f('ix_chat_users_created_at'), table_name='users', schema='chat')
    op.drop_table('users', schema='chat')
    # ### end Alembic commands ###
