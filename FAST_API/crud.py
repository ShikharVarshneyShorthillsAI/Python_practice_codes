from sqlalchemy.orm import Session
from models import UserModel
from schemas import UserCreate

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = self.db.query(UserModel).filter(UserModel.email == user.email).first()
        if db_user:
            return None  # Email already exists

        new_user = UserModel(name=user.name, email=user.email)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_users(self):
        return self.db.query(UserModel).all()
