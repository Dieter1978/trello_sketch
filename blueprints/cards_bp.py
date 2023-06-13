from flask import Blueprint, request
from models.card import Card, CardSchema
from init import db
from flask_jwt_extended import jwt_required
from blueprints.auth_bp import admin_required
from datetime import date

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

# GET convention gets all cards at this route


@cards_bp.route("/")
@jwt_required()
def all_cards():
    admin_required()
    # select * from cards;
    stmt = db.select(Card).order_by(Card.status.desc())
    cards = db.session.scalars(stmt).all()
    return CardSchema(many=True).dump(cards)

# Standard read route for one card as per CRUD


@cards_bp.route('/<int:card_id>')
def one_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card is not None:
        return CardSchema().dump(card)
    else:
        # no card comes back with 404 Not Found
        return {"Error": "No card with this id was found"}, 404

# Create a new card


@cards_bp.route('/', methods=['POST'])
def create_card():
    card_info = CardSchema().load(request.json)
    card = Card(
        title=card_info['title'],
        description=card_info['description'],
        status=card_info['status'],
        date_created=date.today()
    )
    db.session.add(card)
    db.session.commit()
    return CardSchema().dump(card), 201

# Update a card


@cards_bp.route('/<int:card_id>', methods=['PUT', 'PATCH'])
def update_card(card_id):
    stmt = db.select(Card).filter_by(id=card_id)
    card = db.session.scalar(stmt)
    if card is not None:
        card_info = CardSchema().load(request.json)

        card.title = card_info['title'],
        card.description = card_info['description'],
        card.status = card_info['status'],
        card.date_created = date.today()
        # model has been changed now commit the update
        db.session.commit()
        return CardSchema().dump(card), 202
    else:
        # no card comes back with 404 Not Found
        return {"Error": "No card with this id was found"}, 404
