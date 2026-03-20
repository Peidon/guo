import os

class Settings:
    METAL_API_KEY = os.getenv("METAL_API_KEY")
    DB_URL = os.getenv("DATABASE_URL")

settings = Settings()