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

    def get_context_string(self, context: str) -> str:
        """取得根據 `context` 和用戶的密碼、時間資訊組合的字串"""

        # 確保同樣的連結不能再使用第二次
        # 如果之前沒有認證過 (update_at is None) 就用 create_time
        if self.updated_at is None:

            return f"{context}{self.password[-6:]}{self.create_at.strftime('%Y%m%d%H%M%S')}".strip()

        return f"{context}{self.password[-6:]}{self.updated_at.strftime('%Y%m%d%H%M%S')}".strip()
