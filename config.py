import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "fallback-secret")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    @staticmethod
    def get_connection_string():
        database_url = os.getenv("postgresql://roadmap_db_ygum_user:5hnLWVfDmzAT9xOhawrXguJfbII6vYYw@dpg-d6pfr64r85hc73e2m1gg-a/roadmap_db_ygum")
        if database_url:
            if database_url.startswith("postgres://"):
                database_url = database_url.replace("postgres://", "postgresql://", 1)
            return database_url
        return None