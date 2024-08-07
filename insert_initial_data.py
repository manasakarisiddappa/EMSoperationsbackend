from app import create_app
from config.database import db
from models.employee import Employee
from models.department import Department
from models.project import Project

def insert_data():
    app = create_app()
    with app.app_context():
        db.session.add(Department(id=1, name='HR'))
        db.session.add(Department(id=2, name='IT'))
        db.session.add(Department(id=3, name='Dev'))
        db.session.add(Employee(name='John', age=30, department_id=1))
        db.session.add(Employee(name='Jane', age=25, department_id=2))
        db.session.add(Employee(name='Jack', age=26, department_id=3))  
        db.session.add(Project(name='Project A'))
        db.session.add(Project(name='Project B'))
        db.session.add(Project(name='Project C'))
        db.session.commit()

if __name__ == '__main__':
    insert_data()
