from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

error_blueprint = Blueprint("error_page", __name__, "templates")


@error_blueprint.app_errorhandler(Exception)
def handle_error(e):
    if isinstance(e, HTTPException):
        return jsonify(success=False), e.code
    else:

        # В случае серверных ошибок
        return jsonify(success=False, exception=repr(e)), 500
