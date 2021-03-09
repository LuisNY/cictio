import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../'))

from .base import Base

class City(Base):

    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    code = Column(String(8), unique=True, nullable=False)
    country = Column(String(255)) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    people = relationship("Person", back_populates="city")   

    def __init__(self, name, code, country=""):
        self.name = name
        self.code = code
        self.country = country
    
class Person(Base):
    
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    dob = Column(DateTime, nullable=False)
    ssn = Column(Integer, nullable=False, unique=True)
    city_code = Column(String(8), ForeignKey("cities.code"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    city = relationship("City", back_populates="people")

    def __init__(self, first_name, last_name, dob, ssn, city_code):

        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.ssn = ssn
        self.city_code = city_code 
   




