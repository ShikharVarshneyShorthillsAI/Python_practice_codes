from sqlalchemy.orm import Session
from models import UserModel
from schemas import *

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User):
        new_user = UserModel(username=user.name, password=user.password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_users(self):
        return self.db.query(UserModel).all()
    
    # 0 for success
    # 1 for username not found
    # 2 for password is wrong
    def check_user_password(self,user:User) -> int:

        db_user = self.db.query(UserModel).filter(UserModel.username == user.name).first()
        if db_user is None:
            return 1
        elif db_user.password == user.password:
            return 0
        else:
            return 2
        
    def check_user_exists(self,user:User)-> bool:
        db_user = self.db.query(UserModel).filter(UserModel.username == user.name).first()
        
        if db_user is None:
            return False
        else:
            return True
        
        
