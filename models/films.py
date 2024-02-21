from sqlalchemy import Column, Integer, String, ForeignKey, Table, TypeDecorator
from sqlalchemy.orm import relationship
from database.database_config import Base
from pydantic import BaseModel, Field
from typing import Optional

from models import *

# Define the association table for many-to-many relationship between User and Film
film_user_association = Table(
    "film_user",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("film_id", Integer, ForeignKey("films.id")),
    Column("role", String),  # Additional column for role
    extend_existing=True
)

# Define the association table for many-to-many relationship between User and Company
company_user_association = Table(
    "company_user",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("company_id", Integer, ForeignKey("companies.id")),
    Column("role", String),  # Additional column for role
    extend_existing=True
)


class ListType(TypeDecorator):
    """Custom SQLAlchemy type for storing lists as strings in the database."""

    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)


class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    budget = Column(Integer)
    release_year = Column(Integer)
    genres = ListType(String)
    company_id = Column(Integer, ForeignKey('companies.id'))

    # Establishing the one-to-many relationship with Company table
    company = relationship("Company", back_populates="films")

    # Establishing the many-to-many relationship with User table with role
    users = relationship("User", secondary=film_user_association, back_populates="films")

# pydantic model for data validation.
class FilmSchema(BaseModel):
    title: str
    description: Optional[str] = None
    budget: Optional[int] = None
    release_year: int
    genres: list[str] = Field(None, alias="genres")

# This is a temporary bug-fix for the response validation of user-roles endpoint.
class FilmSchemaWithoutGenres(BaseModel):
    title: str
    description: Optional[str] = None
    budget: Optional[int] = None
    release_year: int
