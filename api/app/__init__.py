from flask import Flask
from flask_migrate import Migrate
from app.blueprints import *
from app.database.base import db
import app.database


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://rr_admin:rr_pass@localhost:5432/rr_data"
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(index)
    app.register_blueprint(user_management, url_prefix="/users")

    return app


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0")
