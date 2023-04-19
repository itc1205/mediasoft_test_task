from flask import Flask, request, render_template

from data import db_session

app = Flask(__name__)

@app.errorhandler(400)
def handle_invalid_request(e):
   pass 


@app.route('/', methods=["GET"])
def index():
    return "Hello, wordlie~!"

def main() -> None:
    db_session.global_init("db/main_db.sqlite")
    app.run(host='0.0.0.0', port=8080)    

if __name__ == "__main__":
    main()