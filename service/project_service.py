from typing import List, Optional
from models.project import ProjectModel
from repository.project_repo import ProjectRepo
from utils.validators import validate_name
from service.base_service import BaseService
from models.schemas import ProjectCreate,ProjectUpdate,ProjectResponse,ProjectResponseWithEmp

class ProjectService(BaseService[ProjectModel]):
    def __init__(self):
        super().__init__(repo=ProjectRepo())

    def get_all_projects(self) -> List[ProjectResponse]:
        return self.repo.get_all_projects()

    def get_project_by_id(self, project_id: int) -> Optional[ProjectResponse]:
        return self.repo.get_project_by_id(project_id)

    def create_project(self, data: ProjectCreate) -> ProjectResponse:
        validate_name(data.name)
        return self.repo.create_project(data)

    def update_project(self, project_id: int, data: ProjectUpdate) -> Optional[ProjectResponse]:
        validate_name(data.name)
        return self.repo.update_project(project_id, data)

    def delete_project(self, project_id: int) -> bool:
        return self.repo.delete_project(project_id)

    def get_project_with_employees(self, project_id: int) -> Optional[ProjectResponseWithEmp]:
        return self.repo.get_project_with_employees(project_id)