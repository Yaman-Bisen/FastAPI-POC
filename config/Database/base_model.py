from datetime import datetime

from sqlalchemy import Boolean, DateTime, func, Integer

from sqlalchemy.sql.dml import Delete
from sqlalchemy.sql import update, Select, select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative

from sqlalchemy.orm import declared_attr, Mapped, mapped_column

# soft delete defination
async def soft_delete(session: AsyncSession, stmt):
    if isinstance(stmt, Delete):
        model = stmt.table
        if hasattr(model.c, 'is_deleted'):
            soft_delete_stmt = update(model).where(stmt.whereclause).values(is_deleted=True, deleted_at=datetime.now())
            return await session.execute(soft_delete_stmt)
    
    return await session.execute(stmt)

async def custom_execute(self, stmt, *args, **kwargs):
    if isinstance(stmt, Delete):
        return await soft_delete(self, stmt)

    if isinstance(stmt, Select):
        model = stmt.froms[0]
        if hasattr(model.c, "is_deleted"):
            stmt = stmt.where(model.c.is_deleted == False) 

    return await self._original_execute(stmt, *args, **kwargs)

async def custom_get(self, model, ident, options=None):
    stmt = select(model).where(model.id == ident)
    if hasattr(model, "is_deleted"):
        stmt = stmt.where(model.is_deleted == False)
    result = await self.execute(stmt)
    return result.scalar_one_or_none()

# patching the functions
AsyncSession._original_execute = AsyncSession.execute
AsyncSession.execute = custom_execute

AsyncSession._original_get = AsyncSession.get
AsyncSession.get = custom_get

@as_declarative()
class BaseModel:
    __abstract__ = True 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True) 

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


mapped_metadata = {
    'default': BaseModel.metadata
}

