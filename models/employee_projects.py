from sqlalchemy import Table, Column, Integer, ForeignKey
from config.database import db
from sqlalchemy.orm import relationship
 
employee_projects = Table('employee_projects', db.Model.metadata,
    Column('employee_id', Integer, ForeignKey('employees.id')),
    Column('project_id', Integer, ForeignKey('projects.id'))
)
 
employee = relationship("Employee", back_populates="projects")
project = relationship("Project", back_populates="employees")