from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime

from .db_session import SqlAlchemyBase

from .city import City

class Street(SqlAlchemyBase):
#########################################################
    __tablename__ = 'streets'
#########################################################
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    city: Mapped["City"] = relationship()
    #shops: Mapped[List["Shop"]] = relationship()

#########################################################
    city_id : Mapped[int] = mapped_column(ForeignKey("cities.id"))

