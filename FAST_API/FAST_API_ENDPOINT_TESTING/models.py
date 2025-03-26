from sqlalchemy import Column, Integer, String
from database import db_instance

class UserModel(db_instance.Base):
    __tablename__ = "username_password"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False,unique = True)
    password = Column(String(100), nullable=False)
