from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from extensions.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)

    username = db.Column(db.String(100),unique=True,nullable=False)

    email = db.Column(db.String(255),unique=True,nullable=False)

    password_hash = db.Column(db.String(255),nullable=False)

    role = db.Column(db.String(50),nullable=False,default="user")

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )
        
    password_hash = db.Column(
    db.String(255),
    nullable=False
)