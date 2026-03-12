import os
from dotenv import load_dotenv



load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "4c2efafd33b7668f1d2a962c41bf9c72aa652e2f44f5c5fecb1ff11a2711fb31")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DB_SERVER = os.getenv("DB_SERVER", "PANDU")
    DB_NAME = os.getenv("DB_NAME", "roadmap_db")
    DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

    @staticmethod
    def get_connection_string():
        cfg = Config
        driver = cfg.DB_DRIVER.replace(' ', '+')
        return (
            f"mssql+pyodbc://@{cfg.DB_SERVER}/{cfg.DB_NAME}"
            f"?driver={driver}"
            f"&trusted_connection=yes"
        )