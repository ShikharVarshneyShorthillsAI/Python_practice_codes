from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_instance
from schemas import UserCreate, UserResponse
from crud import UserService
from fastapi.responses import FileResponse

class UserAPI:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/users/", self.create_user, methods=["POST"], response_model=UserResponse)
        self.router.add_api_route("/users/", self.get_users, methods=["GET"], response_model=list[UserResponse])
        self.router.add_api_route("/favicon.ico", self.get_favicon, methods=["GET"], include_in_schema=False)

    def create_user(self, user: UserCreate, db: Session = Depends(db_instance.get_db)):
        user_service = UserService(db)
        new_user = user_service.create_user(user)
        if not new_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return new_user

    def get_users(self, db: Session = Depends(db_instance.get_db)):
        user_service = UserService(db)
        return user_service.get_users()
    
    def get_favicon(self):
        """Serve the favicon.ico file"""
        return FileResponse("favicon.ico")

# Create an instance of UserAPI
user_api = UserAPI()
