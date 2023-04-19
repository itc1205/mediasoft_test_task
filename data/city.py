from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class City(SqlAlchemyBase):
#########################################################
    __tablename__ = 'city_table'
#########################################################

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    shops: Mapped[List["Shop"]] = relationship(back_populates="city")
    streets: Mapped[List["Street"]] = relationship(back_populates="city")

#########################################################
    #shops: Mapped[List["Shop"]] = relationship(back_populates="cities")
