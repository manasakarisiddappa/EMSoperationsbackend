from pydantic import BaseModel
from typing import List, Optional
 
class DepartmentBase(BaseModel):
    id: int
    name: str
 
    class Config:
        from_attributes = True  
 
class ProjectBase(BaseModel):
    id: int
    name: str
 
    class Config:
        from_attributes = True  
 
# class EmployeeCreate(BaseModel):
#     id: Optional[int] = None
#     name: str
#     age: int
#     department_id: Optional[int] = None
 
#     class Config:
#         from_attributes = True  
 
# schemas.py
 
class EmployeeCreate(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    department_id: Optional[int] = None
    project_id: Optional[int] = None  
 
    class Config:
        from_attributes = True  
 
 
# class EmployeeUpdate(BaseModel):
#     name: Optional[str] = None
#     age: Optional[int] = None
#     department_id: Optional[int] = None
 
#     class Config:
#         from_attributes = True  
 
class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    department_id: Optional[int] = None
    project_id: Optional[int] = None  
 
    class Config:
        from_attributes = True  
 
class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
 
    class Config:
        from_attributes = True  
 
class EmployeeResponseWithDept(BaseModel):
    id: int
    name: str
    age: int
    department: Optional[DepartmentBase] = None
 
    class Config:
        from_attributes = True  
 
class EmployeeResponseWithProj(BaseModel):
    id: int
    name: str
    age: int
    department_id: Optional[int]  
    department: Optional[DepartmentBase] = None
    projects: List[ProjectBase] = []
 
    class Config:
        from_attributes = True  
 
class DepartmentCreate(BaseModel):
    id: Optional[int] = None
    name: str
 
class DepartmentUpdate(BaseModel):
    name: Optional[str]
 
class EmployeeBase(BaseModel):
    id: int
    name: str
    age: int
 
    class Config:
        from_attributes = True  
 
class DepartmentResponse(BaseModel):
    id: int
    name: str
 
    class Config:
        from_attributes = True  
 
class DepartmentResponseWithEmp(BaseModel):
    id: int
    name: str
    employees: Optional[List[EmployeeBase]] = []
 
    class Config:
        from_attributes = True  
 
class ProjectCreate(BaseModel):
    id: Optional[int] = None
    name: str
 
class ProjectUpdate(BaseModel):
    name: Optional[str]
 
class ProjectResponse(BaseModel):
    id: int
    name: str
 
    class Config:
        from_attributes = True  
 
class ProjectResponseWithEmp(BaseModel):
    id: int
    name: str
    employees: Optional[List[EmployeeBase]] = []
    departments: Optional[List[DepartmentBase]] = []
 
    class Config:
        from_attributes = True  
 