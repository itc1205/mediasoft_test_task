from flask import Blueprint, jsonify


index_blueprint = Blueprint("index_blueprint", __name__, "templates")


@index_blueprint.route('/', methods=["GET"])
def index():
    return jsonify(success=True, status=200), "Content-Type = application/json"
