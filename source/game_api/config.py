import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/labap_db")
SECRET_KEY = os.getenv("SECRET_KEY", "1234")
SQLALCHEMY_TRACK_MODIFICATIONS = False
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "password")

RARITY_LEVELS = [1, 2, 3, 4, 5]
BASE_WEIGHTS = [50, 25, 15, 7, 3]  # Corresponding weights for rarity levels
REWARDS = [5, 10, 15, 20, 25]  # Rewards for catching monsters of each rarity level