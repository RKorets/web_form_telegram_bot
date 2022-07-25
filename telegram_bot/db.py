from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('mysql+pymysql://root:password@localhost:3306/web_form', echo=False)
metadata = Base.metadata
DBSession = sessionmaker(bind=engine)
session = DBSession()