from init import db, ma
from marshmallow import fields


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    description = db.Column(db.Text())
    status = db.Column(db.String(30))
    date_created = db.Column(db.Date())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='cards')


class CardSchema(ma.Schema):
    # This will serialize the user field as JSON
    user = fields.Nested('UserSchema', exclude=['password', 'cards'])

    class Meta:
        # Fields to expose
        fields = ("id", "title", "description",
                  "status",  "date_created",  "user")
        ordered = True
