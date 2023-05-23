from flask import Blueprint, request, abort, render_template, jsonify
from sqlalchemy import and_, or_

from jsonschema import validate, ValidationError

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Query

from data import db_session
from data.models import City
from data.models import Street
from data.models import Shop

from datetime import datetime as dt

shop_blueprint = Blueprint("shop_blueprint", __name__,
                           "templates", url_prefix='/shop')


shop_example = {
    "shop": {
        "name": str(),
        "city": int(),
        "street": int(),
        "house": int(),
        "opening_time": str(),
        "closing_time": str()
    }
}

schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "city": {
            "type": "number",
            "minimum": 0,
        },
        "street": {
            "type": "number",
            "minimum": 0,
        },
        "house": {
            "type": "number",
            "minimum": 0,
        },
        "opening_time": {
            "type": "string"
        },
        "closing_time": {
            "type": "string"
        }
    },
    "required": ["name", "city", "street", "house", "opening_time", "closing_time"]
}

DATE_FORMAT = "%H:%M"


def __check_if_fields_are_same(data: dict, example_data: dict) -> bool:
    # Проверяем на наличие всех ключей
    print(not (len(data) == len(example_data) and all(
        key in data for key in example_data)))
    if not (len(data) == len(example_data) and all(key in data for key in example_data)):
        return False
    # Проверяем на типы всех ключей
    if not all(type(example_data[key]) == type(data[key]) for key in example_data):
        return False
    return True


def __is_dict_correct(data: dict, example_data: dict) -> bool:
    check_passed = __check_if_fields_are_same(data, example_data)
    if not check_passed:
        return False

    for key in example_data.keys():
        if key not in data:
            return False

        if isinstance(data[key], dict):
            if not __is_dict_correct(data[key], example_data[key]):
                return False

    return True


def check_for_data_correctness(data: dict) -> bool:
    """Функция для проверки правильности типов и ключей в сыром json'е"""
    if data == None:
        return False

    # check_passed = is_dict_correct(data, shop_example)

    try:
        validate(data["shop"], schema)
    except (TypeError, ValidationError) as e:
        return False

    try:
        # Чисто в теории мы могли бы возвращать наше время и оптимизировать время запроса но эээаааээ
        dt.strptime(data["shop"]["opening_time"], DATE_FORMAT)
    except ValueError:
        return False

    try:
        dt.strptime(data["shop"]["closing_time"], DATE_FORMAT)
    except ValueError:
        return False

    return True


def check_if_shop_exists(shop_data: dict, session: scoped_session) -> bool:
    shop = session.query(Shop).join(City).join(Street).filter(
        and_(
            Shop.name == shop_data["name"],
            City.id == shop_data["city"],
            Street.id == shop_data["street"],
            Shop.house == shop_data["house"]
        )
    ).first()

    if shop:
        return True
    return False


def get_city(shop_data: dict, session: scoped_session) -> City:

    city = session.query(City).filter(City.id == shop_data["city"]).first()

    return city


def get_street(shop_data: dict, city: City, session: scoped_session) -> Street:
    street = session.query(Street).filter(
        Street.id == shop_data["street"]).first()

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

    if city == None or street == None:
        abort(400)

    shop = Shop()
    shop.name = data["shop"]["name"]
    shop.city = city
    shop.street = street
    shop.house = data["shop"]["house"]
    shop.opening_time = dt.strptime(
        data["shop"]["opening_time"], "%H:%M").time()
    shop.closing_time = dt.strptime(
        data["shop"]["closing_time"], "%H:%M").time()

    session.add(shop)
    session.flush()

    session.commit()

    return jsonify(success=True, shop_id=shop.id)


def dictify_shop(shop: Shop, session: scoped_session) -> dict:
    shop_as_dict = shop.as_dict()
    shop_as_dict['city'] = session.get(City, shop_as_dict["city_id"]).name
    shop_as_dict['street'] = session.get(
        Street, shop_as_dict["street_id"]).name
    shop_as_dict['opening_time'] = shop_as_dict['opening_time'].strftime(
        DATE_FORMAT)
    shop_as_dict['closing_time'] = shop_as_dict['closing_time'].strftime(
        DATE_FORMAT)

    return shop_as_dict


def is_open(_open: str) -> bool:
    if _open == None:
        return True
    try:
        _open = int(_open)
    except ValueError:
        return False
    if _open not in (0, 1):
        return False
    return True


def filter_streets(street: str, q_shops: Query[Shop]) -> Query[Shop]:
    if street == None:
        return q_shops
    return q_shops.join(Street).filter(Street.id == street)


def filter_cities(city: str, q_shops: Query[Shop]) -> Query[Shop]:
    if city == None:
        return q_shops
    return q_shops.join(City).filter(City.id == city)


def filter_time(_open: str, q_shops: Query[Shop]) -> Query[Shop]:
    if _open == None:
        return q_shops
    server_time = dt.now().time()

    _open = int(_open)

    if _open == 0:  # Closed
        return q_shops.filter(or_(
            Shop.closing_time < server_time,
            Shop.opening_time > server_time
        ))
    elif _open == 1:  # Open
        return q_shops.filter(and_(
            Shop.closing_time >= server_time,
            Shop.opening_time <= server_time
        ))


@shop_blueprint.route("/", methods=["GET"])
def get_shops():
    street = request.args.get("street")
    city = request.args.get("city")
    opened = request.args.get("open")

    if not is_open(opened):
        abort(400)

    session = scoped_session(db_session.create_session())
    q_shops = session.query(Shop)
    q_shops = filter_streets(street, q_shops)
    q_shops = filter_cities(city, q_shops)

    q_shops = filter_time(opened, q_shops)
    shops = []

    if q_shops != None:
        for shop in q_shops:
            shops.append(dictify_shop(shop, session))
    else:
        abort(400)
    return jsonify(success=True, shops=shops)
