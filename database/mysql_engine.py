from database.db_url import set_mysql_url  #set_mysql_url is a function that creates the schema 'db_pos' in MYSQL instance if schema doesn't exist and returns a string adress to 'db_pos' in MYSQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData

url = set_mysql_url()

engine = create_engine(url)

Session = sessionmaker(bind = engine)
session = Session()

Base = declarative_base()

# metadata = MetaData()



