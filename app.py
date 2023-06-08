from flask import Flask, jsonify, request, abort
from datetime import date
import json
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from os import environ
from dotenv import load_dotenv
from models.user import User, UserSchema
from models.card import Card, CardSchema
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import db_commands

load_dotenv()


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')


db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
app.register_blueprint(db_commands)


def admin_required():
    user_email = get_jwt_identity()
    stmt = db.select(User).filter_by(email=user_email)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401)  # Unauthorised


@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You must be admin to access this'}, 401


cards_schema = CardSchema(many=True)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/register', methods=['POST'])
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
# @app.route("/cards", methods=["GET"])
# def get_cards():
    # get all the cards from the database table
 #   cards_list = Card.query.all()
    # return the data in JSON format
  #  result = cards_schema.dump(cards_list)
  #  return jsonify(result)


@app.route('/login', methods=['POST'])
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


@app.route("/cards")
@jwt_required()
def all_cards():
    admin_required()
    # select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
