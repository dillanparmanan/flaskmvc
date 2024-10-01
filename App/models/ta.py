from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Ta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    
   # username =  db.Column(db.String(20), nullable=False, unique=True)
   # password = db.Column(db.String(120), nullable=False)

    def __init__(self, firstname, lastname, email, course_id = None ):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        #self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.firstname
        }

 #   def set_password(self, password):
 #       """Create hashed password."""
 #       self.password = generate_password_hash(password)
    
 #   def check_password(self, password):
 #       """Check hashed password."""
 #       return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Ta {self.id} - {self.firstname} - {self.lastname}>'