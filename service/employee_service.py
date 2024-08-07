from typing import Optional
from repository.employee_repo import EmployeeRepo
from models.schemas import EmployeeCreate, EmployeeUpdate, EmployeeResponse, EmployeeResponseWithDept,EmployeeResponseWithProj
from utils.validators import validate_name, validate_age, validate_department_id

class EmployeeService:
    def __init__(self):
        self.repo = EmployeeRepo()

    def get_all_employees(self) -> Optional[EmployeeResponse]:
        return self.repo.get_all_employees()

    def get_employee_by_id(self, employee_id: int) -> Optional[EmployeeResponse]:
        return self.repo.get_employee_by_id(employee_id)

    def create_employee(self, data: EmployeeCreate) -> EmployeeResponse:
        validate_name(data.name)
        validate_age(data.age)
        validate_department_id(data.department_id)
        return self.repo.create_employee(data)

    def update_employee(self, employee_id: int, data: EmployeeUpdate) -> Optional[EmployeeResponse]:
        validate_name(data.name)
        validate_age(data.age)
        validate_department_id(data.department_id)
        return self.repo.update_employee(employee_id, data)

    def delete_employee(self, employee_id: int) -> bool:
        return self.repo.delete_employee(employee_id)

    def get_employee_with_department(self, employee_id: int) -> Optional[EmployeeResponseWithDept]:
        return self.repo.get_employee_with_department(employee_id)

    def get_employee_with_projects(self, employee_id: int) -> Optional[EmployeeResponseWithProj]:
        return self.repo.get_employee_with_projects(employee_id)
