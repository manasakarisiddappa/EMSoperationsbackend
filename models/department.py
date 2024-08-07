from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import db
from pydantic import BaseModel, Field
 
class Department(db.Model):
    __tablename__ = 'departments'
 
    # id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
 
    # Relationships
    employees = relationship("Employee", back_populates="department")
   
 
class DepartmentModel(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the department")