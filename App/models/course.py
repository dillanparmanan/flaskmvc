from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    lecturers = db.relationship('Lecturer', backref='course', lazy=True, cascade="all, delete-orphan")
    tas = db.relationship('Ta', backref='course', lazy=True, cascade="all, delete-orphan")
    tutors = db.relationship('Tutor', backref='course', lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'Course {self.id} - {self.name} - {self.username} - {self.lecturers} - {self.tas} - {self.tutors}'