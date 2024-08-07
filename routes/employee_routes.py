from typing import Dict, Any
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from service.employee_service import EmployeeService
from service.project_service import ProjectService
from service.department_service import DepartmentService
from utils.response_controller import success_response, error_response
from models.schemas import EmployeeCreate, EmployeeUpdate, DepartmentCreate, DepartmentUpdate, ProjectCreate, ProjectUpdate

routes_bp = Blueprint('routes_bp', __name__)

def handle_service_errors(func):
    """Decorator to handle errors from service functions."""
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return error_response(f"Invalid data: {e}", 400)
        except ValueError as e:
            return error_response(f"Validation error: {e}", 400)
        except Exception as e:
            return error_response(f"An error occurred: {e}", 500)
    return wrapper

def create_model_from_request(model_class: Any) -> Any:
    """Helper function to create a model instance from request JSON."""
    try:
        return model_class(**request.json)
    except ValidationError as e:
        raise ValueError(f"Validation error: {e}")  
    except TypeError as e:
        raise ValueError(f"Error creating instance model: {e}")  

employee_service = EmployeeService()
project_service = ProjectService()
department_service = DepartmentService()

# Employee Routes
@routes_bp.route('/employees', methods=['GET'], endpoint='get_all_employees')
@handle_service_errors
def get_employees() -> Dict[str, Any]:
    employees = employee_service.get_all_employees()
    return success_response([employee.dict() for employee in employees]) if employees else error_response("No employees found", 404)

@routes_bp.route('/employees/<int:employee_id>', methods=['GET'], endpoint='get_employee_by_id')
@handle_service_errors
def get_employee(employee_id: int) -> Dict[str, Any]:
    employee = employee_service.get_employee_by_id(employee_id)
    return success_response(employee.dict()) if employee else error_response("Employee not found", 404)

@routes_bp.route('/employees', methods=['POST'], endpoint='create_employee')
@handle_service_errors
def create_employee() -> Dict[str, Any]:
    data = create_model_from_request(EmployeeCreate)
    employee = employee_service.create_employee(data)
    return success_response(employee.dict(), "Employee created successfully", 201)

@routes_bp.route('/employees/<int:employee_id>', methods=['PUT'], endpoint='update_employee')
@handle_service_errors
def update_employee(employee_id: int) -> Dict[str, Any]:
    data = create_model_from_request(EmployeeUpdate)
    employee = employee_service.update_employee(employee_id, data)
    return success_response(employee.dict(), "Employee updated successfully") if employee else error_response("Employee not found", 404)

@routes_bp.route('/employees/<int:employee_id>', methods=['DELETE'], endpoint='delete_employee')
@handle_service_errors
def delete_employee(employee_id: int) -> Dict[str, Any]:
    if employee_service.delete_employee(employee_id):
        return success_response(None, "Employee deleted successfully")
    return error_response("Employee not found", 404)

@routes_bp.route('/employees/<int:employee_id>/department', methods=['GET'], endpoint='get_employee_with_department')
@handle_service_errors
def get_employee_with_department(employee_id: int) -> Dict[str, Any]:
    result = employee_service.get_employee_with_department(employee_id)
    return success_response(result.dict()) if result else error_response("Employee or Department not found", 404)

@routes_bp.route('/employees/<int:employee_id>/projects', methods=['GET'], endpoint='get_employee_with_projects')
@handle_service_errors
def get_employee_with_projects(employee_id: int) -> Dict[str, Any]:
    result = employee_service.get_employee_with_projects(employee_id)
    return success_response(result.dict()) if result else error_response("Employee or Projects not found", 404)

# Department Routes
@routes_bp.route('/departments', methods=['GET'], endpoint='get_all_departments')
@handle_service_errors
def get_departments() -> Dict[str, Any]:
    departments = department_service.get_all_departments()
    return success_response([department.dict() for department in departments]) if departments else error_response("No departments found", 404)

@routes_bp.route('/departments/<int:department_id>', methods=['GET'], endpoint='get_department_by_id')
@handle_service_errors
def get_department(department_id: int) -> Dict[str, Any]:
    department = department_service.get_department_by_id(department_id)
    return success_response(department.dict()) if department else error_response("Department not found", 404)

@routes_bp.route('/departments', methods=['POST'], endpoint='create_department')
@handle_service_errors
def create_department() -> Dict[str, Any]:
    data = create_model_from_request(DepartmentCreate)
    department = department_service.create_department(data)
    return success_response(department.dict(), "Department created successfully", 201)

@routes_bp.route('/departments/<int:department_id>', methods=['PUT'], endpoint='update_department')
@handle_service_errors
def update_department(department_id: int) -> Dict[str, Any]:
    data = create_model_from_request(DepartmentUpdate)
    department = department_service.update_department(department_id, data)
    return success_response(department.dict(), "Department updated successfully") if department else error_response("Department not found", 404)

@routes_bp.route('/departments/<int:department_id>', methods=['DELETE'], endpoint='delete_department')
@handle_service_errors
def delete_department(department_id: int) -> Dict[str, Any]:
    if department_service.delete_department(department_id):
        return success_response(None, "Department deleted successfully")
    return error_response("Department not found", 404)

@routes_bp.route('/departments/<int:department_id>/employees', methods=['GET'], endpoint='get_department_with_employees')
@handle_service_errors
def get_department_with_employees(department_id: int) -> Dict[str, Any]:
    result = department_service.get_department_with_employees(department_id)
    return success_response(result.dict()) if result else error_response("Department or Employees not found", 404)

# Project Routes
@routes_bp.route('/projects', methods=['GET'], endpoint='get_all_projects')
@handle_service_errors
def get_projects() -> Dict[str, Any]:
    projects = project_service.get_all_projects()
    return success_response([project.dict() for project in projects]) if projects else error_response("No projects found", 404)

@routes_bp.route('/projects/<int:project_id>', methods=['GET'], endpoint='get_project_by_id')
@handle_service_errors
def get_project(project_id: int) -> Dict[str, Any]:
    project = project_service.get_project_by_id(project_id)
    return success_response(project.dict()) if project else error_response("Project not found", 404)

@routes_bp.route('/projects', methods=['POST'], endpoint='create_project')
@handle_service_errors
def create_project() -> Dict[str, Any]:
    data = create_model_from_request(ProjectCreate)
    project = project_service.create_project(data)
    return success_response(project.dict(), "Project created successfully", 201)

@routes_bp.route('/projects/<int:project_id>', methods=['PUT'], endpoint='update_project')
@handle_service_errors
def update_project(project_id: int) -> Dict[str, Any]:
    data = create_model_from_request(ProjectUpdate)
    project = project_service.update_project(project_id, data)
    return success_response(project.dict(), "Project updated successfully") if project else error_response("Project not found", 404)

@routes_bp.route('/projects/<int:project_id>', methods=['DELETE'], endpoint='delete_project')
@handle_service_errors
def delete_project(project_id: int) -> Dict[str, Any]:
    if project_service.delete_project(project_id):
        return success_response(None, "Project deleted successfully")
    return error_response("Project not found", 404)

@routes_bp.route('/projects/<int:project_id>/employees', methods=['GET'], endpoint='get_project_with_employees')
@handle_service_errors
def get_project_with_employees(project_id: int) -> Dict[str, Any]:
    result = project_service.get_project_with_employees(project_id)
    return success_response(result.dict()) if result else error_response("Project or Employees not found", 404)
