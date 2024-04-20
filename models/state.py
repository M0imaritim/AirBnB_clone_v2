#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel,Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
import models
from models.city import City
from sqlalchemy.ext.declarative import declarative_base


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """ returns the list of City instances with state_id
        equals to the current State.id"""
        from models import storage
        city_instances = []
        cities = storage.all(City)
        for city in cities.values():
            if city.state_id == self.id:
                city_instances.append(city)
        return city_instances
