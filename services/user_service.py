from models.user import User
from repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def validate_password(password):
        if len(password) < 8:
            raise ValueError(
                "Password must be at least 8 characters long"
            )

        if not any(char.isupper() for char in password):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not any(char.islower() for char in password):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not any(char.isdigit() for char in password):
            raise ValueError(
                "Password must contain at least one digit"
            )

        special_characters = "!@#$%^&*()-_=+[]{};:,.?/\\|"

        if not any(
            char in special_characters
            for char in password
        ):
            raise ValueError(
                "Password must contain at least one special character"
            )
    
    @staticmethod
    def validate_role(role):
        allowed_roles = {
            "admin",
            "doctor",
            "receptionist",
            "user"
        }

        if role not in allowed_roles:
            raise ValueError(
                "Invalid role. Allowed roles are: admin, doctor, receptionist, user"
            )
            
            
    @staticmethod
    def create_user_by_admin(data):
        username = data["username"]
        email = data["email"]
        password = data["password"]
        role = data.get("role", "user")

        # Password validation
        UserService.validate_password(password)

        # Role validation
        UserService.validate_role(role)

        # Duplicate username check
        existing_username = UserRepository.get_by_username(username)

        if existing_username:
            raise ValueError("Username already exists")

        # Duplicate email check
        existing_email = UserRepository.get_by_email(email)

        if existing_email:
            raise ValueError("Email already exists")

        # Create user with selected role
        user = User(
            username=username,
            email=email,
            role=role
        )

        user.set_password(password)

        return UserRepository.create(user)

    @staticmethod
    def register_user(data):
        username = data["username"]
        email = data["email"]
        password = data["password"]

        # Password validation
        UserService.validate_password(password)

        # Duplicate username check
        existing_username = UserRepository.get_by_username(username)

        if existing_username:
            raise ValueError("Username already exists")

        # Duplicate email check
        existing_email = UserRepository.get_by_email(email)

        if existing_email:
            raise ValueError("Email already exists")

        # Create user
        user = User(
        username=username,
        email=email,
        role="user"
                 )
        user.set_password(password)

        return UserRepository.create(user)

    @staticmethod
    def get_all_users():
        return UserRepository.get_all()