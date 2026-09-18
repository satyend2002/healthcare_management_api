from extensions.extensions import db
from models.department import Department


class DepartmentRepository:

    # Get all departments ..................
    @staticmethod
    def get_all():
        return Department.query.all()


    # Get department by ID ................
    @staticmethod
    def get_by_id(department_id):
        return db.session.get(Department, department_id)


    # Get department by name ..................
    @staticmethod
    def get_by_name(name):
        return Department.query.filter_by(
            name=name
        ).first()


    # Get department by name excluding current department ......
    @staticmethod
    def get_by_name_excluding_id(name, department_id):
        return Department.query.filter(
            Department.name == name,
            Department.id != department_id
        ).first()


    # Create department .................
    @staticmethod
    def create(department):
        db.session.add(department)
        db.session.commit()

        return department


    # Update department  ....................
    @staticmethod
    def update(department):
        db.session.commit()

        return department


    # Delete department  ................
    @staticmethod
    def delete(department):
        db.session.delete(department)
        db.session.commit()