from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from app.config.database import Base


class User(Base):
    """使用者資料資料表"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(150), nullable=False)
    password = Column(String(128))
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    create_at = Column(DateTime, nullable=False, server_default=func.now())
