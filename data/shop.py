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
    __tablename__ = 'shops'
#########################################################    

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column() 
    city: Mapped["City"] = relationship()
    street: Mapped["Street"] = relationship()
    home: Mapped[int] = mapped_column() #Дом обозначается в цифровом представлении
    opening_time: Mapped[dt.time] = mapped_column()
    closing_time: Mapped[dt.time] = mapped_column()   

#########################################################
    city_id : Mapped[int] = mapped_column(ForeignKey("cities.id"))
    street_id : Mapped[int] = mapped_column(ForeignKey("streets.id"))