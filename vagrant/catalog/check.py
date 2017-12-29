from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item

engine = create_engine('sqlite:///item_catalog.db')
DBSession = sessionmaker(bind=engine)
session = DBSession()

print session.query(Category).all()
print ''
print session.query(Item).all()
