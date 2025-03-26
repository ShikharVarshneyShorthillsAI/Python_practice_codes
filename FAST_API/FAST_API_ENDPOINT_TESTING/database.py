from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import config

class Database:
    def __init__(self):
        self.engine = create_engine(config.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Database instance
db_instance = Database()
