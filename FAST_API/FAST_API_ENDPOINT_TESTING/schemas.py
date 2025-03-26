from pydantic import BaseModel,ConfigDict

class User(BaseModel):
    name: str
    password: str

class UserResponse(User):
    id: int

    class Config:
        from_attributes = True  # Enable ORM mode

class Login_result(BaseModel):
    result:str

class Sign_up_result(BaseModel):
    result :str


