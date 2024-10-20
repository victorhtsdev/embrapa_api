import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    db_url = os.getenv('DATABASE_URL')

    # Adaptaçao para Heroku
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True