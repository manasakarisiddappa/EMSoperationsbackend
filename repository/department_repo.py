from typing import Optional, List
from sqlalchemy.orm import joinedload
from models.department import Department
from config.database import db
from sqlalchemy.exc import IntegrityError
from models.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse, EmployeeBase, ProjectBase, DepartmentResponseWithEmp
 
class DepartmentRepo:
 
    def _get_department_by_id(self, department_id: int) -> Optional[Department]:
        """Helper method to get a department by its ID."""
        return db.session.query(Department).filter(Department.id == department_id).first()
 
    def _map_to_department_response(self, department: Department) -> DepartmentResponse:
        """Map a Department object to a response model."""
        return DepartmentResponse(
            id=department.id,
            name=department.name
        )
   
    def _map_to_department_response_with_emp_and_proj(self, department: Department) -> DepartmentResponseWithEmp:
        """Map a Department object to a response model with employees and projects."""
        return DepartmentResponseWithEmp(
            id=department.id,
            name=department.name,
            employees=[EmployeeBase(id=emp.id, name=emp.name, age=emp.age) for emp in department.employees] if department.employees else [],
            projects=[ProjectBase(id=proj.id, name=proj.name) for proj in department.projects] if department.projects else []
        )
 
    def get_all_departments(self) -> List[DepartmentResponse]:
        """Retrieve all departments."""
        departments = db.session.query(Department).all()
        return [self._map_to_department_response(dept) for dept in departments]
   
    def get_department_by_id(self, department_id: int) -> Optional[DepartmentResponse]:
        """Retrieve a department by its ID."""
        department = self._get_department_by_id(department_id)
        return self._map_to_department_response(department) if department else None
   
    def create_department(self, data: DepartmentCreate) -> DepartmentResponse:
        """Create a new department."""
        existing_department = db.session.query(Department).filter(Department.name == data.name).first()
        if existing_department:
            raise ValueError(f"Department with the name '{data.name}' already exists.")
        department = Department(id=data.id, name=data.name) if data.id else Department(name=data.name)
        db.session.add(department)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise
        return self._map_to_department_response(department)
   
    def update_department(self, department_id: int, data: DepartmentUpdate) -> Optional[DepartmentResponse]:
        """Update a department by its ID."""
        department = self._get_department_by_id(department_id)
        if department:
            if data.name is not None:
                department.name = data.name
           
            db.session.commit()
            return self._map_to_department_response(department)
       
        return None
   
    def delete_department(self, department_id: int) -> bool:
        """Delete a department by its ID."""
        department = self._get_department_by_id(department_id)
        if department:
            db.session.delete(department)
            db.session.commit()
            return True
        return False
   
    def get_department_with_employees_and_projects(self, department_id: int) -> Optional[DepartmentResponseWithEmp]:
        """Retrieve a department with its employees and projects."""
        department = db.session.query(Department).options(joinedload(Department.employees), joinedload(Department.projects)).filter(Department.id == department_id).first()
        return self._map_to_department_response_with_emp_and_proj(department) if department else None