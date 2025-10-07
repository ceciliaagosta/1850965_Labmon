import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/labap_db")
SECRET_KEY = os.getenv("SECRET_KEY", "1234")
SQLALCHEMY_TRACK_MODIFICATIONS = False
TTL_ACCESS_TOKEN = 7200  # 2 hours
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "localhost")