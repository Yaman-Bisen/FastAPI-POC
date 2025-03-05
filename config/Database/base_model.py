from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.sql import func, select
from datetime import datetime
from config.settings import settings

@as_declarative()
class BaseModel:
    __abstract__ = True 

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    is_deleted: Mapped[bool] = mapped_column(default=False)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


mapped_metadata = {
    'default': BaseModel.metadata
}