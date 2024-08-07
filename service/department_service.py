from typing import Optional, List
from repository.department_repo import DepartmentRepo
from utils.validators import validate_name
from models.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentResponseWithEmp

class DepartmentService:
    def __init__(self):
        self.repo = DepartmentRepo()

    def get_all_departments(self) -> List[DepartmentResponse]:
        return self.repo.get_all_departments()

    def get_department_by_id(self, department_id: int) -> Optional[DepartmentResponse]:
        return self.repo.get_department_by_id(department_id)

    def create_department(self, data: DepartmentCreate) -> DepartmentResponse:
        validate_name(data.name)
        return self.repo.create_department(data)

    def update_department(self, department_id: int, data: DepartmentUpdate) -> Optional[DepartmentResponse]:
        validate_name(data.name)
        return self.repo.update_department(department_id, data)

    def delete_department(self, department_id: int) -> bool:
        return self.repo.delete_department(department_id)

    def get_department_with_employees(self, department_id: int) -> Optional[DepartmentResponseWithEmp]:
        return self.repo.get_department_with_employees(department_id)
