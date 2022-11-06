import os


class Config(object):
    PYTHONPATH = os.getenv("PYTHONPATH", "/usr/src/app")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    ENV = os.getenv("ENV")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INITIAL_SLEEP_SECS = os.getenv("INITIAL_SLEEP_SECS")
    SLEEP_MINS = os.getenv("SLEEP_MINS")
    BASE_API_URI = "https://0lexplorer.io"
    ASSETS_DIR = f"{PYTHONPATH}/crawler/assets"
