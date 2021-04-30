from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.blueprints import *
from app.database.base import db
from app.config import DB_CONNECTION_STRING
import app.database


def create_app():
    app = Flask(__name__)
    CORS(app)
    print(f'CONNECTING TO {DB_CONNECTION_STRING}')
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = DB_CONNECTION_STRING
    db.init_app(app)
    app.db = db
    migrate = Migrate(app, db)

    app.register_blueprint(index)
    app.register_blueprint(user_management, url_prefix="/users")

    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0")
