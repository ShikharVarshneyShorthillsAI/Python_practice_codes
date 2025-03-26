from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import db_instance
from schemas import *
from crud import UserService
from fastapi.responses import FileResponse
from typing import Any, Dict

import json

class UserAPI:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/echo_input",self.echo_input,methods=["POST"],response_model = Dict[str,Any])
        self.router.add_api_route("/login",self.login,methods=["GET"],response_model = Login_result)
        self.router.add_api_route("/signup",self.signup,methods=["POST"],response_model = Sign_up_result)

    async def echo_input(self,request:Dict[str,Any]):
        return request  
    
    async def login(self,request:User,db: Session = Depends(db_instance.get_db)):
        service = UserService(db)
        if  not request.name.strip() and not request.password.strip() :
            return Login_result(result="Username and Password cannot be empty")
        if not request.name.strip():
            return Login_result(result="Username cannot be empty")
        
        if not request.password.strip():
            return Login_result(result="Password cannot be empty")

        return_value = service.check_user_password(request)
        if  return_value == 0:
            return Login_result(result = "Login Successful")
        elif return_value == 1:
            return Login_result(result = "Username not found")
        else:
            return Login_result(result = "Password is incorrect")
        
    async def signup(self,request:User,db :Session = Depends(db_instance.get_db)):
        service = UserService(db)
        if  not request.name.strip() and not request.password.strip() :
            return Sign_up_result(result="Username and Password cannot be empty")
        if not request.name.strip():
            return Sign_up_result(result="Username cannot be empty")
        
        if not request.password.strip():
            return Sign_up_result(result="Password cannot be empty")
        
        if service.check_user_exists(request):
            return Sign_up_result(result="Username is already taken")
        else:
            new_user = service.create_user(request)
            return Sign_up_result(result="Signed up successfully")
                
            
        

# Create an instance of UserAPI
user_api = UserAPI()
