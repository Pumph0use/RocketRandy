import json

from flask import Blueprint, current_app, request
from app.database import User

user_management = Blueprint("user_management", __name__)


@user_management.route("/<int:member_id>", methods=['GET'])
def get_user(member_id):
    print(f'MEMBER ID: {member_id}')
    print(f'MEMBER ID TYPE: {type(member_id)}')
    user = User.query.filter(User.id == member_id).first()

    print(f'USER: {user}')
    print(f'USER TYP: {type(user)}')

    if user:
        user = {'id': user.id, 'display_name': user.display_name}
        return json.dumps(user), 200, {'Content-Type': 'application/json'}
    else:
        return 'User not found', 404


@user_management.route('/', methods=['POST'])
def add_user():
    content = request.json
    if content and all(key in ['id', 'display_name'] for key in content.keys()):
        user = User.query.filter(User.id == content['id']).first()

        if user:
            return json.dumps({'status': 'User already exists'}), 400, {'Content-Type': 'application/json'}
        else:
            user = User()
            user.id = content['id']
            user.display_name = content['display_name']
            current_app.db.session.add(user)
            current_app.db.session.commit()
            return '', 204
    else:
        return json.dumps({'status': 'Bad request'}), 400, {'Content-Type': 'application/json'}

