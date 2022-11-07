"""Create SQLAlchemy engine and session objects."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Create database engine
engine = create_engine(os.getenv("DATABASE_URL"))

# Create database session
Session = sessionmaker(bind=engine)
session = Session()
