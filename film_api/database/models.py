"""Module with database models"""
import os

from decimal import Decimal
from sqlalchemy import (Column,
                        ForeignKey,
                        Integer,
                        Numeric,
                        String,
                        Text,
                        DateTime,
                        Boolean,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_CONN_STR = os.getenv('DB_CONN_STR')

if DB_CONN_STR is None:
    DB_CONN_STR = 'sqlite:///dev.sqlite'

engine = create_engine(DB_CONN_STR)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Init db and update created models to the metadata"""
    Base.metadata.create_all(bind=engine)


class Role(Base):
    """Role model class"""
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50))


class Country(Base):
    """Country model class"""
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True)
    country = Column(String(50), nullable=False)

    def __init__(self, country: str):
        self.country = country


class User(Base):
    """User model class"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    role_id = Column(ForeignKey('roles.role_id'))
    name = Column(String(50))
    surname = Column(String(50))
    country_id = Column(ForeignKey('countries.country_id'))
    password = Column(String(50), nullable=False)
    is_authenticated = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_anonymous = Column(Boolean, nullable=False)
    api_key = Column(String(36), nullable=False)


    def __init__(self, username: str, role_id: int = None, name: str = None,
                 surname: str = None):
        self.username = username
        self.role_id = role_id
        self.name = name
        self.surname = surname


class Genres(Base):
    """Genre model class"""
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column(String(50), nullable=False)
    description = Column(Text)

    def __init__(self, genre_name: str, description: str = None):
        self.genre_name = genre_name
        self.description = description



class Producer(Base):
    """Producer model class"""
    __tablename__ = 'producers'

    producer_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    birth_date = Column(DateTime)
    country_id = Column(ForeignKey('countries.country_id'))

    def __init__(self, name: str, surname: str, birth_date: str = None,
                 country_id: int = None):
        self.name = name
        self.surname = surname
        self.birth_date = birth_date
        self.country_id = country_id


class Film(Base):
    """Film model class"""
    __tablename__ = 'films'

    film_id = Column(Integer, primary_key=True)
    film_title = Column(String(100), nullable=False)
    release_date = Column(DateTime, nullable=False)
    producer_id = Column(ForeignKey('producers.producer_id'))

    description = Column(Text)
    rating = Column(Numeric(4, 2))
    poster = Column(Text, nullable=False)
    created_by = Column(ForeignKey('users.user_id'), nullable=False)

    def __init__(self, film_title: str, release_date: str, poster, created_by,
                 producer_id: int = None, description: str = None,
                 rating: Decimal = None):
        self.film_title = film_title
        self.release_date = release_date
        self.producer_id = producer_id
        self.description = description
        self.rating = rating
        self.poster = poster
        self.created_by = created_by


class FilmGenre(Base):
    """Films and genres proxy table"""
    __tablename__ = 'films_genres'

    film_id = Column(Integer, primary_key=True)
    genre_id = Column(Integer, primary_key=True)

    def __init__(self, film_id: int, genre_id: int):
        self.film_id = film_id
        self.genre_id = genre_id
