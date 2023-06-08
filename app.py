from flask import Flask
from os import environ
from dotenv import load_dotenv
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.cards_bp import cards_bp

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
app.register_blueprint(cards_bp)


@app.errorhandler(401)
def unauthorized(err):
    return {'error': 'You must be admin to access this'}, 401


if __name__ == '__main__':
    app.run(debug=True, port=3000)
