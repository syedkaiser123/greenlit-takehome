from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from database.database_config import Base
from .films import film_user_association, company_user_association, FilmSchemaWithoutGenres
from .companies import CompanySchema

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    minimum_fee = Column(Integer)

    # Establishing many-to-many relationship with Film table
    films = relationship("Film", secondary=film_user_association, back_populates="users")
    
    # Establishing many-to-many relationship with Company table
    companies = relationship("Company", secondary=company_user_association, back_populates="users")

# Pydantic model for data validation
class UserSchema(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    minimum_fee: int = Field(..., ge=0)

    class Config:
        orm_mode = True

class UserRoleSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    minimum_fee: int
    films: list[FilmSchemaWithoutGenres]
    companies: list[CompanySchema]
