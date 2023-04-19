from flask import Flask, request, render_template

from data import db_session

from error_handlers import error_blueprint

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html.j2")

def main() -> None:
    db_session.global_init("db/main_db.sqlite")
    app.register_blueprint(error_blueprint)
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()