from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_CONNECT_STRING

engine = create_engine(DB_CONNECT_STRING, echo=True)
Session = sessionmaker(bind=engine)
