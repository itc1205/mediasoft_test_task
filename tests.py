from data import db_session

import datetime as dt

from data.city import City
from data.shop import Shop
from data.street import Street

def test_city():
    db_session.global_init("db/main_db.sqlite")
    session_maker = db_session.create_session()
    session = session_maker()
    city = City()
    city.name = "Ul'yanovsk"
    session.add(city)
    session.commit()

def test_street():
    db_session.global_init("db/main_db.sqlite")
    session_maker = db_session.create_session()
    session = session_maker()
    city = session.query(City).filter(City.name == "Ul'yanovsk").first()
    street = Street()
    street.name = "Ryabikova"
    street.city = city
    session.add(street)
    session.commit()

def test_shop():
    db_session.global_init("db/main_db.sqlite")
    session_maker = db_session.create_session()
    session = session_maker()
    city = session.query(City).filter(City.name == "Ul'yanovsk").first()
    street = session.query(Street).filter(Street.name == "Ryabikova").first()
    shop = Shop()
    
    shop.city = city
    shop.street = street
    shop.home = 60
    shop.name = "Magnit"
    shop.opening_time = dt.datetime.now().time()
    shop.closing_time = dt.datetime.now().time()
    session.add(shop)
    session.commit()

if __name__ == "__main__":
    test_city()
    test_street()
    test_shop()