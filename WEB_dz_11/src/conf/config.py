import os
from dotenv import load_dotenv

load_dotenv()
password = os.getenv('DB_PASSWORD')
user = os.getenv('DB_USERNAME')
name = os.getenv('DB_NAME')


class Config:
    DB_URL = f'postgresql+asyncpg://{user}:{password}@localhost:5432/{name}'


config = Config
