from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://cictio_user:cictio@localhost/cictio_db", echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()

def createAll():
    Base.metadata.create_all(engine)

def getSession():
    return Session()