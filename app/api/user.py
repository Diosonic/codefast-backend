from flask import request, jsonify
from app.api import bp
from app.models import User
from app import db


@bp.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    
    users_dict = [user.to_dict() for user in users]

    return jsonify(users_dict)


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    requireds = ['name', 'email']
    absent = [field for field in requireds if field not in data]

    if len(absent) > 0:
        raise Exception('Fields requireds')
    
    user = User()

    user.from_dict(data)
    db.session.add(user)
    db.session.commit()

    return jsonify({'oret': user.to_dict()}), 201

    
