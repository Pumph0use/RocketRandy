from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:Pumph0use!!@localhost:5432/rocketrandy", echo=True)
Session = sessionmaker(bind=engine)
