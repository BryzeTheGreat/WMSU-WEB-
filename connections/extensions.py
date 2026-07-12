from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask_mail import Mail

engine = create_engine('sqlite:///database/data.db')

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
mail = Mail()
