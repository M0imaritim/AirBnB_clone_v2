#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Table, String, Integer, Float, ForeignKey
import models
from os import getenv

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete,\
                               delete-orphan', backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            """
            returns the list of Review instances with place_id
            equals to the current Place.id
            """
            all_reviews = storage.all("Review")
            place_reviews = []
            for review in all_reviews.values():
                if review.place_id == self.id:
                    place_reviews.append(review)
            return place_reviews

        @property
        def amenities(self):
            """Getter attribute to return amenities associated with the place"""
            all_amenities = storage.all("Amenity")
            place_amenities = []
            for amenity_id in self.amenity_ids:
                amenity = all_amenities.get(amenity_id)
                if amenity:
                    place_amenities.append(amenity)
            return place_amenities

        @amenities.setter
        def amenities(self, obj):
            """handles append method for adding an Amenity.id to
            the attribute amenity_ids"""
            if isinstance(obj, Amenity):
                if amenity.id not in self.amenity_ids:
                    self.amenity_ids.append(amenity.id)
