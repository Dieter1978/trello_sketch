from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://trello_dev:spameggs123@localhost:5432/trello'

db.init_app(app)

print(db.__dict__)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text())
    date_created = db.Column(db.Date())


@app.cli.command('create')
def create_db():
    db.create_all()
    print('Tables created successfully')


@app.cli.command('drop')
def create_db():
    db.drop_all()
    print('Tables dropped successfully')


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, port=3000)
