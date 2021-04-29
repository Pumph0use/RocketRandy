from .base import db


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    display_name = db.Column(db.String(32))
