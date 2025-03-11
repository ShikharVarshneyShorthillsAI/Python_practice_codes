from fastapi import FastAPI
from database import db_instance
from api import user_api

class FastAPIApp:
    def __init__(self):
        self.app = FastAPI()
        self.setup_database()
        self.include_routes()

    def setup_database(self):
        """Create database tables"""
        db_instance.Base.metadata.create_all(bind=db_instance.engine)

    def include_routes(self):
        """Include all API routers"""
        self.app.include_router(user_api.router)

    def get_app(self):
        """Return the FastAPI application"""
        return self.app

# Create an instance of FastAPIApp
app_instance = FastAPIApp()
app = app_instance.get_app()
