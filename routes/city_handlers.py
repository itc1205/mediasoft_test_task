from flask import Blueprint, render_template

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Query

from data import db_session
from data.city import City
from data.street import Street


city_blueprint = Blueprint("city_blueprint", __name__, "templates", url_prefix='/city')


def get_cities_from_db() -> Query:
    session = scoped_session(db_session.create_session())
    cities = session.query(City)
    return cities


@city_blueprint.route('/', methods=["GET"])
def get_cities():
    cities = get_cities_from_db()
    return render_template("cities.html.j2", cities=cities)



def get_streets_from_db(city_id: int):
    session = scoped_session(db_session.create_session())
    streets = session.query(Street).filter(Street.city_id == city_id)
    return streets

@city_blueprint.route('/<int:city_id>/street/', methods=["GET"])
def get_streets(city_id:int):
    streets = get_streets_from_db(city_id)
    return render_template("streets.html.j2", streets=streets)
