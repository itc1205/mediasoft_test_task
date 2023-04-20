from flask import Flask

from data import db_session

from routes.city_handler import city_blueprint
from routes.error_handler import error_blueprint
from routes.index_handler import index_blueprint
from routes.shop_handler import shop_blueprint

from dotenv import load_dotenv

import configure_env

app = Flask(__name__)

    
def main() -> None:
    db_session.global_init("db/main_db.sqlite")
    app.register_blueprint(city_blueprint)
    app.register_blueprint(error_blueprint)
    app.register_blueprint(index_blueprint)
    app.register_blueprint(shop_blueprint)
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    if not load_dotenv(".env"):
        print("Внимание, файл .env недоступены. Запускаю средство для создания .env")
        configure_env.setup()
    if not load_dotenv(".env"):
        raise Exception("Невозможно загрузить .env!")
    main()