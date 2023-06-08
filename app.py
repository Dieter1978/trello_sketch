from flask import Flask, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from os import environ
from dotenv import load_dotenv
from models.user import User
from models.card import Card, CardSchema
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp

load_dotenv()


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')


db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
app.register_blueprint(cli_bp)
app.register_blueprint(auth_bp)


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
