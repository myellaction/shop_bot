import os
from dotenv import load_dotenv

load_dotenv()

TOKEN_API = str(os.getenv('TOKEN_API'))
DB_NAME = str(os.getenv('DB_NAME'))
DB_PASS = str(os.getenv('DB_PASS'))
DB_USER = str(os.getenv('DB_USER'))
DB_HOST = str(os.getenv('DB_HOST'))