from flask import Blueprint, request, abort
from sqlalchemy import and_

from werkzeug.exceptions import HTTPException
from werkzeug import Response

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Query

from data import db_session
from data.city import City
from data.street import Street
from data.shop import Shop

from datetime import datetime as dt

shop_blueprint = Blueprint("shop_blueprint", __name__, "templates", url_prefix='/shop')

shop_json_keys = {
    "name",
    "city",
    "street",
    "house",
    "opening_time",
    "closing_time"
}

def check_for_data_correctness(data: dict) -> bool:
    #Проверяем получили ли мы наш json'чик правильно
    if data == None:
        return False
    if "shop" not in data.keys():
        return False
    if shop_json_keys != data["shop"].keys():
        print("incorrect keys", data["shop"].keys(), shop_json_keys)
        return False
    if not isinstance(data["shop"]["name"], str):
        return False
    if not isinstance(data["shop"]["city"], str):
        return False
    if not isinstance(data["shop"]["street"], str):
        return False
    if not isinstance(data["shop"]["house"], int):
        return False
    if not isinstance(data["shop"]["opening_time"], str):
        return False
    if not isinstance(data["shop"]["closing_time"], str):
        return False
    
    try:
        dt.strptime(data["shop"]["opening_time"], "%H:%M")
    except ValueError:
        return False
    
    try:
        dt.strptime(data["shop"]["closing_time"], "%H:%M")
    except ValueError:
        return False

    return True

def check_if_shop_exists(shop_data: dict, session: scoped_session) -> bool:
    print("OK")
    print(shop_data)
    shop = session.query(Shop).join(City).join(Street).filter(
        and_(
            Shop.name == shop_data["name"],
            City.name == shop_data["city"],
            Street.name == shop_data["street"],
            Shop.house == shop_data["house"]
        )
    ).first()
    
    if shop:
        return True
    return False

def get_city(shop_data:dict, session: scoped_session) -> City:
    """Функция для получения города (если его не существует, создаем и закидываем в очередь коммита для базы данных)"""
   
    city = session.query(City).filter(City.name == shop_data["city"]).first()
    
    if city == None:
        city = City()
        city.name = shop_data["city"]
        session.add(city)
    
    return city

def get_street(shop_data:dict, city: City,session: scoped_session) -> Street:
    """Функция для получения улицы (если ее не существует, создаем и закидываем в очередь коммита для базы данных)"""
    street = session.query(Street).filter(Street.name == shop_data["street"]).first()
    
    if street == None:
        street = Street()
        street.name = shop_data["street"]
        street.city = city
        session.add(street)
    
    return street

@shop_blueprint.route("/", methods=["POST"])
def create_new_shop():
    data = request.get_json()
    if not check_for_data_correctness(data):
        abort(400)
        

    session = scoped_session(db_session.create_session())
    if check_if_shop_exists(data["shop"], session):
        abort(400)
    city = get_city(data["shop"], session)
    street = get_street(data["shop"], city, session)
    
    shop = Shop()
    shop.name = data["shop"]["name"]
    shop.city = city
    shop.street = street
    shop.house = data["shop"]["house"]
    shop.opening_time = dt.strptime(data["shop"]["opening_time"], "%H:%M").time()
    shop.closing_time = dt.strptime(data["shop"]["closing_time"], "%H:%M").time()
    
    session.add(shop)
    session.commit()
    
    return ""