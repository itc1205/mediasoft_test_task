from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

errors = {
 404 : {
    "number" : 404,
    "name" : "Страница не найдена",
    "description" : "Вероятнее всего вы попали не на ту страницу"
 },
 400 : {
   "number" : 400,
   "name" : "Неверный запрос",
   "description" : "Вероятнее всего вы неверно оформили запрос"
 }
}

error_blueprint = Blueprint("error_page", __name__, "templates")

   
@error_blueprint.app_errorhandler(Exception)
def handle_error(e):
   if isinstance(e, HTTPException):
      error = errors[e.code]
      return render_template("error.html.j2", **error), error["number"]
   else:
      return 'Something really reallyyyyy fucked up', e #В случае серверных ошибок