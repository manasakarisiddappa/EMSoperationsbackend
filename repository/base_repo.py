from typing import List, Dict, Any, Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepo(Generic[T]):
    def __init__(self, model: T, session: Session):
        self.model = model
        self.session = session

    def get_all(self) -> List[Dict[str, Any]]:
        return [self._map_to_dict(item) for item in self.session.query(self.model).all()]

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        item = self.session.query(self.model).get(entity_id)
        return self._map_to_dict(item) if item else None

    def create(self, data: T) -> Dict[str, Any]:
        item = self.model(**data.dict())
        self.session.add(item)
        self.session.commit()
        return self._map_to_dict(item)

    def update(self, entity_id: int, data: T) -> Optional[Dict[str, Any]]:
        item = self.session.query(self.model).get(entity_id)
        if item:
            for field, value in data.dict(exclude_unset=True).items():
                setattr(item, field, value)
            self.session.commit()
            return self._map_to_dict(item)
        return None

    def delete(self, entity_id: int) -> bool:
        item = self.session.query(self.model).get(entity_id)
        if item:
            self.session.delete(item)
            self.session.commit()
            return True
        return False

    def _map_to_dict(self, item) -> Dict[str, Any]:
        return {column.name: getattr(item, column.name) for column in self.model.__table__.columns}
