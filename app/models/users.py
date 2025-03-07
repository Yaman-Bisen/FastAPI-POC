from sqlalchemy.orm import Mapped, mapped_column
from config.Database.base_model import BaseModel

class Users(BaseModel):
    __tablename__ = "user_db1"

    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
