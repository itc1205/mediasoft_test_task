from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship

import datetime as dt

from .db_session import SqlAlchemyBase

from .city import City
from .street import Street

class Shop(SqlAlchemyBase):
#########################################################
    __tablename__ = 'shop_table'
#########################################################    

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column() 
    city: Mapped["City"] = relationship(back_populates="shops")
    street: Mapped["Street"] = relationship(back_populates="shops")
    house: Mapped[int] = mapped_column() #Дом обозначается в цифровом представлении
    opening_time: Mapped[dt.time] = mapped_column()
    closing_time: Mapped[dt.time] = mapped_column()   

#########################################################
    city_id : Mapped[int] = mapped_column(ForeignKey("city_table.id"))
    street_id : Mapped[int] = mapped_column(ForeignKey("street_table.id"))
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}