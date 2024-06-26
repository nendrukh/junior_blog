import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как нет файла .env")
else:
    load_dotenv()

API_KEY: str = os.getenv("API_KEY")
SECRET_KEY: str = os.getenv("SECRET_KEY")
