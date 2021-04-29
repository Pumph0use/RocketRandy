import json

from flask import Blueprint, current_app

index = Blueprint("index", __name__)


@index.route("/")
def health_check():
    return json.dumps({"status": "OK"}), 200, {"Content-Type": "application/json"}
