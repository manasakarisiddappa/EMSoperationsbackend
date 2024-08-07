from flask import jsonify
from typing import Any, Dict

def create_response(msg: str, status_code: int, data: Any) -> Dict[str, Any]:
    if not isinstance(data, (dict, list, str, int, float, type(None))):
        raise ValueError("Invalid data type provided for response")
    
    return {
        "msg": msg,
        "status_code": status_code,
        "data": data
    }

def success_response(data: Any = None, msg: str = "Success", status_code: int = 200) -> tuple:
    response = create_response(msg, status_code, data)
    return jsonify(response), status_code

def error_response(msg: str = "Error", status_code: int = 400) -> tuple:
    response = create_response(msg, status_code, None)
    return jsonify(response), status_code
