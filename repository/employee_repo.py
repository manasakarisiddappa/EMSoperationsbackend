from typing import Optional, List
from sqlalchemy.orm import joinedload
from models.employee import Employee
from models.project import Project
from models.employee_projects import employee_projects
from config.database import db
from models.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeResponseWithDept, EmployeeResponseWithProj, DepartmentBase, ProjectBase
 
class EmployeeRepo:
    def _get_employee_by_id(self, employee_id: int) -> Optional[Employee]:
        return db.session.query(Employee).filter(Employee.id == employee_id).first()
 
    def _map_to_employee_response(self, employee: Employee, include_projects: bool = True) -> EmployeeResponse:
        return EmployeeResponse(
            id=employee.id,
            name=employee.name,
            age=employee.age,
        )
 
    def _map_to_employee_response_with_dept(self, employee: Employee) -> EmployeeResponseWithDept:
        return EmployeeResponseWithDept(
            id=employee.id,
            name=employee.name,
            age=employee.age,
            department=DepartmentBase(
                id=employee.department.id,
                name=employee.department.name
            ) if employee.department else None
        )
 
    def _map_to_employee_response_with_proj(self, employee: Employee) -> EmployeeResponseWithProj:
        return EmployeeResponseWithProj(
            id=employee.id,
            name=employee.name,
            age=employee.age,
            department_id=employee.department.id if employee.department else None,
            department=DepartmentBase(
                id=employee.department.id,
                name=employee.department.name
            ) if employee.department else None,
            projects=[ProjectBase(id=project.id, name=project.name) for project in employee.projects] if employee.projects else []
        )
 
    def get_all_employees(self) -> List[EmployeeResponse]:
        employees = db.session.query(Employee).all()
        return [self._map_to_employee_response(employee) for employee in employees]
 
    def get_employee_by_id(self, employee_id: int) -> Optional[EmployeeResponseWithProj]:
        employee = db.session.query(Employee).options(joinedload(Employee.department), joinedload(Employee.projects)).filter(Employee.id == employee_id).first()
        if employee:
            return self._map_to_employee_response_with_proj(employee)
        return None
 
    def create_employee(self, data: EmployeeCreate) -> EmployeeResponse:
        employee = Employee(
            name=data.name,
            age=data.age,
            department_id=data.department_id
        )
        db.session.add(employee)
        db.session.flush()  # Ensures that the employee gets an ID before the commit
 
        if data.project_id:
            employee_project = employee_projects.insert().values(
                employee_id=employee.id,
                project_id=data.project_id
            )
            db.session.execute(employee_project)
 
        db.session.commit()
        return self._map_to_employee_response(employee)
 
    # def update_employee(self, employee_id: int, data: EmployeeUpdate) -> Optional[EmployeeResponse]:
    #     employee = self._get_employee_by_id(employee_id)
    #     if employee:
    #         for key, value in data.dict().items():
    #             setattr(employee, key, value)
    #         db.session.commit()
    #         return self._map_to_employee_response(employee)
    #     return None
 
    def update_employee(self, employee_id: int, data: EmployeeUpdate) -> Optional[EmployeeResponse]:
        employee = self._get_employee_by_id(employee_id)
        if employee:
            for key, value in data.dict().items():
                if key == "project_id" and value is not None:
                    project = db.session.query(Project).filter(Project.id == value).first()
                    if not project:
                        project = Project(id=value, name=f"Project {value}")
                        db.session.add(project)
                        db.session.flush()
                    db.session.execute(
                        employee_projects.delete().where(employee_projects.c.employee_id == employee_id)
                    )
                    employee_project = employee_projects.insert().values(
                        employee_id=employee_id,
                        project_id=value
                    )
                    db.session.execute(employee_project)
                elif value is not None:  
                    setattr(employee, key, value)
 
            db.session.commit()
            return self._map_to_employee_response(employee)
        return None
 
    def delete_employee(self, employee_id: int) -> bool:
        employee = self._get_employee_by_id(employee_id)
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return True
        return False
 
    def get_employee_with_department(self, employee_id: int) -> Optional[EmployeeResponseWithDept]:
        employee = db.session.query(Employee).options(joinedload(Employee.department)).filter(Employee.id == employee_id).first()
        if employee:
            return self._map_to_employee_response_with_dept(employee)
        return None
 
    def get_employee_with_projects(self, employee_id: int) -> Optional[EmployeeResponseWithProj]:
        employee = db.session.query(Employee).options(joinedload(Employee.projects)).filter(Employee.id == employee_id).first()
        if employee:
            return self._map_to_employee_response_with_proj(employee)
        return None