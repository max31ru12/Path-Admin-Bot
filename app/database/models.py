from datetime import datetime

from sqlalchemy import text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db_config import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    link: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)

    notified_one_day: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
    notified_two_hours: Mapped[bool] = mapped_column(default=False, server_default=text("false"))
