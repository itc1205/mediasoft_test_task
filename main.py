from flask import Flask, request, render_template

from data import db_session

from routes.city_handlers import city_blueprint
from routes.error_handlers import error_blueprint
from routes.index import index_blueprint
from routes.shop_handlers import shop_blueprint

app = Flask(__name__)

    
def main() -> None:
    db_session.global_init("db/main_db.sqlite")
    app.register_blueprint(city_blueprint)
    app.register_blueprint(error_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(shop_blueprint)
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()