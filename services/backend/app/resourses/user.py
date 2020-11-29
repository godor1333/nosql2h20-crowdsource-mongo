from flask import Flask, request, Response, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from app.db.models import User

users = Blueprint('users', __name__)

@users.route('/signup', methods=['POST'])
def registration():
    body = request.get_json()
    user = User(**body)
    user.hash_password()
    user.save()
    id = user.id
    return {'id': str(id)}, 200

@users.route('/login',methods=['POST'])
def login():
    body = request.get_json()
    user = User.objects.get(email=body.get('email'))
    authorized = user.check_password(body.get('password'))
    if not authorized:
        return {'error': 'Email or password invalid'}, 401

    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)
    return {'token': access_token, 'user_id': str(user.id)}, 200

@users.route('/<id>',methods=['GET'])
@jwt_required
def get_user(id):
    user_id = get_jwt_identity()
    if user_id == id:
        user = User.objects.get(id=id).to_json()
        return Response(user, mimetype="application/json", status=200)
    return {"msg":"it isnt your acc"},401