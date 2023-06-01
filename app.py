from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
import json

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello'

db.init_app(app)
ma = Marshmallow(app)


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text())
    date_created = db.Column(db.Date())


class CardSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "title", "description", "date_created")


cards_schema = CardSchema(many=True)


@app.cli.command('create')
def create_db():
    # db.drop_all()
    db.create_all()
    print('Tables created successfully')


@app.cli.command('drop')
def create_db():
    db.drop_all()
    print('Tables dropped successfully')


@app.cli.command('seed')
def seed_db():
    # Truncate table
    db.session.query(Card).delete()
    # Create an instance of the Card model in memory
    # Add the card to the session (transaction)
    db.session.add(Card(
        title='Start the project',
        description='Create an ERD',
        date_created=date.today()
    ))
    # Commit the transaction to the dabase
    db.session.commit()


@app.route('/')
def index():
    return 'Hello World!'


# @app.route("/cards", methods=["GET"])
# def get_cards():
    # get all the cards from the database table
 #   cards_list = Card.query.all()
    # return the data in JSON format
  #  result = cards_schema.dump(cards_list)
  #  return jsonify(result)

@app.route("/cards")
def all_cards():
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return json.dumps(cards)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
