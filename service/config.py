import os

DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///accounts.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
