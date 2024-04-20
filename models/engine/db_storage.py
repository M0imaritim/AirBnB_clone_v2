#!/usr/bin/python3
"""module defines a new staraage engine"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """class defines DBStorage engine"""
    __engine = None
    __session = None

    def __init__(self):
        """initializes the class"""
        mysql_username = os.environ.get('MYSQL_USERNAME')
        mysql_password = os.environ.get('MYSQL_PASSWORD')
        mysql_host = os.environ.get('MYSQL_HOST')
        mysql_database = os.environ.get('MYSQL_DATABASE')
        hbnb_env = os.environ.get('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                          .format(mysql_username,
                                                  mysql_password,
                                                  mysql_host,  mysql_database),
                                          pool_pre_ping=True)
        if hbnb_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ all objects depending of the class name (argument cls)"""
        objects = {}

        if cls is None:
            classes = [base_model.BaseModel]
        else:
            classes = [cls]

        for clers in classes:
            query = self.__session.query(clers).all()
            for obj in query:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        return objects

    def new(self, obj):
        """adds object to the current db session"""
        session.add(obj)
        session.commit()

    def save(self):
        """commit all changes of the current database session"""
        session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            session.delete(obj)
            session.commit()
        else:
            return

    def reload(self):
        """create all tables in the database """
        Base.metadata.create_all(self.__engine)

        session_maker = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        self.__session = scoped_session(session_maker)
