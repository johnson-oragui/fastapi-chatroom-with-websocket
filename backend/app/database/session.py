"""
Database session module
"""
import asyncio
from typing import AsyncIterator
from sqlalchemy.ext.asyncio import (
    async_scoped_session,       # For creating scoped sessions in async environments
    async_sessionmaker,         # For creating session factories
    AsyncEngine,                # Represents an async engine (connection to DB)
    create_async_engine,        # Preferred way to create async engine
    AsyncSession,               # Represents a session for DB transactions in async context
    AsyncAttrs,                 # Base class for asynchronous ORM mappings
)
from sqlalchemy.orm import (
    DeclarativeBase,  # Base class for ORM models
    Mapped,
    mapped_column,
    declared_attr,
    declarative_mixin
)
from sqlalchemy import (
    MetaData,                   # To define metadata and naming conventions
    pool,
    Table,
    DateTime,
    String,
    func
)
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from datetime import datetime

from app.core.config import settings

naming_convention = {
    "ix": "ix_%(column_0_label)s",                                       # index
    "uq": "uq_%(table_name)s_%(column_0_name)s",                          # unique
    "ck": "ck_%(table_name)s_%(constraint_name)s",                        # constraints
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # foreign key
    "pk": "pk_%(table_name)s"                                             # primary key
}

if settings.test:
    DATABASE_URL = settings.db_url
else:
    DATABASE_URL = settings.db_url_async

class Base(AsyncAttrs, DeclarativeBase):
    if settings.test or "sqlite" in DATABASE_URL:
        metadata = MetaData(
            naming_convention=naming_convention
        )
    else:
        metadata = MetaData(
            schema=settings.db_schema,
            naming_convention=naming_convention
        )
        

# Creates the async engine, use pool_size and max_overflow for control over connections
async_engine: AsyncEngine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
    future=True,
    poolclass=pool.AsyncAdaptedQueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=18000
)

# Create a session factory, ensuring sessions are async
async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)

# Create scoped session tied to async loop
AsyncScoppedSession = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=asyncio.current_task
)

async def create_tables() -> None:
    """
    Creates tables if not already created
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_specific_table(table: Table) -> None:
    """
    Creates a specific tables if not already created
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(table.create)

async def drop_tables() -> None:
    """
    Drops tables if not already dropped
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def drop_specific_table(table: Table) -> None:
    """
    Drops a specific table if not already dropped
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(table.drop)

async def get_session() -> AsyncIterator[AsyncSession]:
    """
    Dependency to provide a database session for each request.
    Handles session lifecycle including commit and rollback.
    """
    async with AsyncScoppedSession() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await AsyncScoppedSession.remove()
            await session.close()

@declarative_mixin
class ModelMixin:
    """
    Mixin Class for ORM Models
    """
    id: Mapped[str] = mapped_column(
        String(60),
        primary_key=True,
        index=True,
        default=lambda:str(uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    @declared_attr
    @classmethod
    def __tablename__(cls):
        """
        Table names
        """
        return f"{cls.__name__.lower()}s"
