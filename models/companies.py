from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.database_config import Base
from pydantic import BaseModel

from .films import company_user_association

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_email_address = Column(String, index=True)
    phone_number = Column(String)

    # Establishing one-to-many relationship with Film table
    films = relationship("Film", back_populates="company")
    
    # Establishing many-to-many relationship with User
    users = relationship("User", secondary=company_user_association, back_populates="companies")

# pydantic model for data validation.
class CompanySchema(BaseModel):
    name: str
    contact_email_address: str
    phone_number: str

