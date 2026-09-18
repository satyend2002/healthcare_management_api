from models.department import Department
from repositories.department_repository import DepartmentRepository


class DepartmentService:

    # Create department
    @staticmethod
    def create_department(data):

        # Check duplicate name
        existing_department = DepartmentRepository.get_by_name(
            data["name"]
        )

        if existing_department:
            return {
                "error": "Department already exists"
            }, 409

        # Create Department object
        department = Department(
            name=data["name"],
            description=data.get("description")
        )

        # Save department
        department = DepartmentRepository.create(department)

        return department


    # Get all departments
    @staticmethod
    def get_all_departments():

        departments = DepartmentRepository.get_all()

        return departments


    # Get department by ID .......
    @staticmethod
    def get_department(department_id):
        department = DepartmentRepository.get_by_id(department_id)
        return department


    # Update department
    @staticmethod
    def update_department(department_id, data):

        # Find department ......
        department = DepartmentRepository.get_by_id(department_id)

        if not department:
            return {
                "message": "Department not found"
            }, 404

        # Check duplicate name .........
        if "name" in data:

            existing_department = (
                DepartmentRepository.get_by_name_excluding_id(
                    data["name"],
                    department_id
                )
            )

            if existing_department:
                return {
                    "message": "Department already exists"
                }, 409

        # Update fields ................
        if "name" in data:
            department.name = data["name"]

        if "description" in data:
            department.description = data["description"]

        # Save updated department .........
        DepartmentRepository.update(department)

        return department


    # Delete department
    @staticmethod
    def delete_department(department_id):

        department = DepartmentRepository.get_by_id(department_id)

        if not department:
            return {
                "message": "Department not found"
            }, 404

        DepartmentRepository.delete(department)

        return {
            "message": "Department deleted successfully"
        }, 200