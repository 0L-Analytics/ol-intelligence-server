import os
import sys

from crawler.db.model import Base, engine


def recreate_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    arg = sys.argv[1]

    if arg == "recreate_datahub_db":
        recreate_db()
