from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import String, Integer

import config
from database.db import Base


class Devs(Base):
    __tablename__ = config.table_name

    dev_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)