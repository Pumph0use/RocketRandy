import os
from dotenv import load_dotenv

if os.getenv('APP_ENV') != 'compose':
    load_dotenv('.env')

DB_TYPE = os.getenv('DB_TYPE')
DB_DRIVER = os.getenv('DB_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DB_CONNECTION_STRING = f'{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
