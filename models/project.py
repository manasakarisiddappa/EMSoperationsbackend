
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.database import db
from models.employee_projects import employee_projects
from pydantic import BaseModel, Field
 
class Project(db.Model):
    __tablename__ = 'projects'
 
    # id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
 
    # Relationships
    employees = relationship("Employee", secondary=employee_projects, back_populates="projects")
   
class ProjectModel(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the project")