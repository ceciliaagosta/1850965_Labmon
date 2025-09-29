from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint



db = SQLAlchemy()

class Item(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    effect = db.Column(db.Float, nullable=False)
    sprite=db.Column(db.String(200), nullable=False)

    def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'price': self.price,
                'description': self.description,
                'effect': self.effect,
                'sprite': self.sprite

            }

    def __repr__(self):
        return str(self.to_dict())
