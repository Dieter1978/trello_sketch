from init import ma, db
from marshmallow import fields


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text())
    date_created = db.Column(db.Date())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    user = db.relationship('User', back_populates='comments')
    card = db.relationship('Card', back_populates='comments')


class CommentSchema(ma.Schema):
    # This will serialize the user field as JSON
    user = fields.Nested('UserSchema', only=['name', 'email'])
    card = fields.Nested('CardSchema', only=['title', 'description', 'status'])

    class Meta:
        # Fields to expose
        fields = ("id", "message", "date_created",  "user", "card")
        ordered = True
