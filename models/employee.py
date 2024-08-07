from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.database import db
from models.department import Department
from models.project import Project
from models.employee_projects import employee_projects
from pydantic import BaseModel, Field
 
class Employee(db.Model):
    __tablename__ = 'employees'
 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    age = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))
 
    # Relationships
    department = relationship("Department", back_populates="employees")
    projects = relationship("Project", secondary=employee_projects, back_populates="employees")
 
class EmployeeModel(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the employee")
    age: int = Field(..., gt=0, description="Age of the employee")
    department_id: int = Field(..., gt=0, description="ID of the department to which the employee belongs")