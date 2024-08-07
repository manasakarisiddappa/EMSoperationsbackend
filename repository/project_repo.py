from typing import Optional, List
from sqlalchemy.orm import joinedload
from models.project import Project
from config.database import db
from sqlalchemy.exc import IntegrityError
from models.schemas import ProjectCreate, ProjectUpdate, ProjectResponse, EmployeeBase, DepartmentBase, ProjectResponseWithEmp
 
class ProjectRepo:
 
    def _get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by its ID."""
        return db.session.query(Project).filter(Project.id == project_id).first()
 
    def get_all_projects(self) -> List[ProjectResponse]:
        """Retrieve all projects."""
        projects = db.session.query(Project).all()
        return [self._map_to_project_response(proj) for proj in projects]
   
    def get_project_by_id(self, project_id: int) -> Optional[ProjectResponse]:
        """Retrieve a project by its ID."""
        project = self._get_project_by_id(project_id)
        return self._map_to_project_response(project) if project else None
   
    # def create_project(self, data: ProjectCreate) -> ProjectResponse:
    #     """Create a project."""
    #     project = Project(id=data.id, name=data.name)
    #     db.session.add(project)
    #     db.session.commit()
    #     return self._map_to_project_response(project)
       
    def create_project(self, data: ProjectCreate) -> ProjectResponse:
        """Create a project."""
        existing_project = db.session.query(Project).filter(Project.name == data.name).first()
        if existing_project:
            raise ValueError(f"A project with the name '{data.name}' already exists.")
        project = Project(id=data.id, name=data.name)
        db.session.add(project)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"An error occurred while creating the project '{data.name}'.")
       
        return self._map_to_project_response(project)
   
    def update_project(self, project_id: int, data: ProjectUpdate) -> Optional[ProjectResponse]:
        """Update a project by its ID."""
        project = self._get_project_by_id(project_id)
        if project:
            if data.name is not None:
                project.name = data.name
            db.session.commit()
            return self._map_to_project_response(project)
        return None
   
    def delete_project(self, project_id: int) -> bool:
        """Delete a project by its ID."""
        project = self._get_project_by_id(project_id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return True
        return False
   
    def get_project_with_employees_and_departments(self, project_id: int) -> Optional[ProjectResponseWithEmp]:
        """Retrieve a project with its associated employees and departments by its ID."""
        project = db.session.query(Project).options(
            joinedload(Project.employees).joinedload("department"),
            joinedload(Project.departments)
        ).filter(Project.id == project_id).first()
        if project:
            return self._map_to_project_response_with_Emp_and_Dept(project)
        return None
 
    def _map_to_project_response(self, project: Project) -> ProjectResponse:
        """Map a project instance to a ProjectResponse object."""
        return ProjectResponse(
            id=project.id,
            name=project.name
        )
   
    def _map_to_project_response_with_Emp_and_Dept(self, project: Project) -> ProjectResponseWithEmp:
        return ProjectResponseWithEmp(
            id=project.id,
            name=project.name,
            employees=[EmployeeBase.from_orm(emp) for emp in project.employees] if project.employees else [],
            departments=[DepartmentBase.from_orm(dept) for dept in project.departments] if project.departments else []
        )
 
