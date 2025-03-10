from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

class Fast_api_hello_world:

    def __init__(self):
        self.app = FastAPI()
        pass
        
    def get_request(self):
        @self.app.get("/")
        async def root():
            return {"message":"hello world"}

        @self.app.get("/favicon.ico",include_in_schema=False)
        async def favicon():
            return FileResponse("favicon.ico")

        @self.app.get("/name_age/{name}/{age}")
        async def name_age(name:str,age:int):
            return {"name":name,"age":age}

        @self.app.get("/hello")
        async def hello(name:str,age:int):
            return {"name":name,"age":age}

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=8000)  # Start the server

if __name__ == "__main__":
    obj = Fast_api_hello_world()
    obj.get_request()
    obj.run()


# to be immplemented
# validation conditions on query and path paramters ,using import path and query



