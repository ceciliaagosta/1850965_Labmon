from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.types import JSON
from datetime import datetime, timezone

db = SQLAlchemy()

# Encounter table
class Encounter(db.Model):
    __tablename__ = 'encounters'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False)
    monster_id = db.Column(db.Integer, nullable=False)
    isCaught = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'player_id': self.player_id,
            'monster_id': self.monster_id,
            'isCaught': self.isCaught,
            'timestamp': self.timestamp,
        }

    def __repr__(self):
        return str(self.to_dict())
    
# Player data table
class Player(db.Model):
    __tablename__ = 'players'

    player_id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.Float, nullable=False, default=200)
    lastEncounter_id = db.Column(db.Integer, nullable=True)
    collections_completed = db.Column(JSON, nullable=False, default=list)

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'currency': self.currency,
            'lastEncounter_id': self.lastEncounter_id,
            'collections_completed': self.collections_completed,
        }

    def __repr__(self):
        return str(self.to_dict())
    
# Collection table
class Collection(db.Model):
    __tablename__ = 'collections'

    # both player_id and monster_id form the composite primary key
    player_id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'monster_id': self.monster_id,
            'qty': self.qty,
        }

    def __repr__(self):
        return str(self.to_dict())
    
# Inventory table
class Inventory(db.Model):
    __tablename__ = 'inventories'

    # both player_id and item_id form the composite primary key
    player_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'item_id': self.item_id,
            'qty': self.qty,
        }

    def __repr__(self):
        return str(self.to_dict())
    
# Monster statistics table
class MonsterStats(db.Model):
    __tablename__ = 'monster_stats'

    monster_id = db.Column(db.Integer, primary_key=True)
    catch_rate = db.Column(db.Float, nullable=False)
    rarity = db.Column(db.Integer, nullable=False)
    collection = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        CheckConstraint('rarity >= 1 AND rarity <= 5', name='rarity_between_1_and_5'),
        CheckConstraint('catch_rate >= 0 AND catch_rate <= 1', name='catch_rate_between_0_and_1'),
    )

    def to_dict(self):
        return {
            'monster_id': self.monster_id,
            'catch_rate': self.catch_rate,
            'rarity': self.rarity,
            'collection': self.collection,
        }

    def __repr__(self):
        return str(self.to_dict())

# Item statistics table
class ItemStats(db.Model):
    __tablename__ = 'item_stats'

    item_id = db.Column(db.Integer, primary_key=True)
    effect = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'price': self.price,
            'effect': self.effect,
        }

    def __repr__(self):
        return str(self.to_dict())