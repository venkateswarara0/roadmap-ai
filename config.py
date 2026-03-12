import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "supersecretkey123")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    @staticmethod
    def get_connection_string():
        database_url = os.getenv("DATABASE_URL", "")
        print(f"DEBUG DATABASE_URL = '{database_url}'")
        if not database_url:
            database_url = "postgresql://roadmap_db_ygum_user:5hnLWVfDmzAT9xOhawrXguJfbII6vYYw@dpg-d6pfr64r85hc73e2m1gg-a/roadmap_db_ygum"
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url