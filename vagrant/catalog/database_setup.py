import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class Category(Base):
    """Category Class create a table named Category"""

    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

    print 'Category Table Created'

class Item(Base):
    """Item Class create a table named item"""

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(300), nullable=False)
    date_added = Column(DateTime, default=datetime.datetime.now)
    cat_id = Column(Integer,ForeignKey('category.id'))
    category = relationship (Category)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'date_added':self.date_added,
        }

    print 'Item Table Created'

engine = create_engine('sqlite:///item_catalog.db')

Base.metadata.create_all(engine)
