from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Monster(db.Model):
    __tablename__ = 'monsters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    rarity = db.Column(db.Integer, nullable=False)
    catch_rate = db.Column(db.Float, nullable=False)
    collection = db.Column(db.Integer, nullable=False)
    sprite = db.Column(db.String(200), nullable=False)

    __table_args__ = (
        CheckConstraint('rarity >= 1 AND rarity <= 5', name='rarity_between_1_and_5'),
        CheckConstraint('catch_rate >= 0 AND catch_rate <= 1', name='catch_rate_between_0_and_1'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'rarity': self.rarity,
            'catch_rate': self.catch_rate,
            'collection': self.collection,
            'sprite': self.sprite
        }

    def __repr__(self):
        return str(self.to_dict())