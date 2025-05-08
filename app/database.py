from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into the environment

# Get the DATABASE_URL environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Heroku gives 'postgres://' but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Establish a connection to the PostgreSQL database
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#
# # Create a cursor object to interact with the database
# cur = conn.cursor()
#
# # Close the cursor and connection
# cur.close()
# conn.close()