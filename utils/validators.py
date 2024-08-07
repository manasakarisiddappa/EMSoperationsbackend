def validate_name(name):
    if not name.strip():
        raise ValueError('Name cannot be blank')

def validate_age(age):
    if not (21 <= age <= 100):
        raise ValueError('Age must be between 21 and 100')

def validate_department_id(department_id):
    if department_id <= 0:
        raise ValueError('Department id cannot be zero')
