from flask import Blueprint, request, abort
from models.user import User, UserSchema
from init import db, bcrypt
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

auth_bp = Blueprint('auth', __name__)


def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)  # Unauthorised


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        user_info = UserSchema().load(request.json)
        user = User(
            email=user_info['email'],
            password=bcrypt.generate_password_hash(
                user_info['password']).decode('utf8'),
            name=user_info['name']
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)

        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(
                identity=user.email, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401
    except KeyError:
        return {'error': 'Email and password are required'}, 400
