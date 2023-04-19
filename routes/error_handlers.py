from flask import Blueprint, render_template
from werkzeug.exceptions import HTTPException

errors = {
 404 : {
    "name" : "Страница не найдена",
    "description" : "Вероятнее всего вы попали не на ту страницу"
 },
 400 : {
   "name" : "Неверный запрос",
   "description" : "Вероятнее всего вы неверно оформили запрос"
 },
 500 : {
   "name" : "Серверу конец",
   "description" : "Помянем прод"
 }
}

error_blueprint = Blueprint("error_page", __name__, "templates")

   
@error_blueprint.app_errorhandler(Exception)
def handle_error(e):
   if isinstance(e, HTTPException):
      error = errors[e.code]
      return render_template("error.html.j2", number=e.code, **error), e.code
   else:
      return render_template("error.html.j2", number=500, name=errors[500]["name"], description=e) #В случае серверных ошибок