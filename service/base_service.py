from typing import List, Dict, Any, Optional, TypeVar, Generic
from repository.base_repo import BaseRepo
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseService(Generic[T]):
    def __init__(self, repo: BaseRepo[T]):
        self.repo = repo

    def get_all(self) -> List[Dict[str, Any]]:
        return self.repo.get_all()

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(entity_id)

    def create(self, data: T) -> Dict[str, Any]:
        return self.repo.create(data)

    def update(self, entity_id: int, data: T) -> Optional[Dict[str, Any]]:
        return self.repo.update(entity_id, data)

    def delete(self, entity_id: int) -> bool:
        return self.repo.delete(entity_id)
