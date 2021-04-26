import os
from dotenv import load_dotenv

load_dotenv()
DB_TYPE = os.getenv('DB_TYPE')
DB_DRIVER = os.getenv('DB_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_URL = os.getenv('DB_URL')
DB_NAME = os.getenv('DB_NAME')
DB_CONNECT_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_URL}/{DB_NAME}"