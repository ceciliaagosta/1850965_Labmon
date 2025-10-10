import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/labap_db")
SECRET_KEY = os.getenv("SECRET_KEY", "1234")
SQLALCHEMY_TRACK_MODIFICATIONS = False
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")  
RABBITMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER", "user")
RABBITMQ_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", "password")