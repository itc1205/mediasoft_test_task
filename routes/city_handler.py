from flask import Blueprint, render_template, abort, jsonify

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Query

from data import db_session
from data.models import Street, City

city_blueprint = Blueprint("city_blueprint", __name__,
                           "templates", url_prefix='/city')


def get_cities_from_db() -> Query:
    session = scoped_session(db_session.create_session())
    cities = session.query(City)
    return cities


@city_blueprint.route('/', methods=["GET"])
def get_cities():
    cities = get_cities_from_db()
    cities_array = [city.as_dict() for city in cities]

    return jsonify(cities_array)


def get_streets_from_db(city_id: int, session):
    streets = session.query(Street).filter(Street.city_id == city_id)
    return streets


def jsonify_street(street: Street, session) -> dict:
    street_json = street.as_dict()
    street_json['city_name'] = session.get(City, street_json["city_id"]).name
    return street_json


@city_blueprint.route('/<int:city_id>/street/', methods=["GET"])
def get_streets(city_id: int):
    session = scoped_session(db_session.create_session())
    streets = get_streets_from_db(city_id, session)
    if streets == None:
        abort(400)
    streets_array = [jsonify_street(street, session) for street in streets]

    return jsonify(streets_array)
