import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    ENV = os.getenv("ENV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
