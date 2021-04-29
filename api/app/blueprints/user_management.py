from flask import Blueprint, current_app
from app.database import User

user_management = Blueprint("user_management", __name__)


@user_management.route("/")
def get_user():
    return "User Management OK"
